import time
import structlog
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential
from graph.state import ProductionState

logger = structlog.get_logger()
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

CATEGORIES = ["기술지원", "결제", "배송", "기타"]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
def _call_llm(messages: list):
    """Rate Limit 대응 retry 래퍼"""
    return llm.invoke(messages)


def classify_question(state: ProductionState) -> dict:
    """[노드 1] 질문 분류 — try/except + 구조화 로깅 적용"""
    start = time.time()
    node_name = "classify_question"
    correlation_id = state.get("correlation_id", "unknown")

    try:
        user_message = state["messages"][-1].content

        response = _call_llm([
            SystemMessage(content="질문을 분류하세요. 다음 중 하나만 출력: 기술지원, 결제, 배송, 기타"),
            HumanMessage(content=user_message),
        ])

        category = response.content.strip()
        if category not in CATEGORIES:
            category = "기타"

        logger.info("node_success", node=node_name, category=category,
                    latency_ms=round((time.time() - start) * 1000),
                    correlation_id=correlation_id)

        return {
            "category": category,
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }

    except Exception as e:
        logger.error("node_error", node=node_name, error=str(e),
                     latency_ms=round((time.time() - start) * 1000),
                     correlation_id=correlation_id)
        return {
            "category": "기타",
            "error": f"{node_name} 실패: {e}",
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }


def generate_answer(state: ProductionState) -> dict:
    """[노드 2] 답변 생성 — 에러 상태 확인 후 처리"""
    start = time.time()
    node_name = "generate_answer"
    correlation_id = state.get("correlation_id", "unknown")

    if state.get("error"):
        return {
            "answer": "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }

    try:
        user_message = state["messages"][-1].content
        category = state.get("category", "기타")

        response = _call_llm([
            SystemMessage(content=(
                f"당신은 고객 지원 챗봇입니다. 카테고리: {category}. "
                "질문에 친절하게 한국어로 답변하세요."
            )),
            HumanMessage(content=user_message),
        ])

        logger.info("node_success", node=node_name,
                    latency_ms=round((time.time() - start) * 1000),
                    correlation_id=correlation_id)

        return {
            "answer": response.content,
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }

    except Exception as e:
        logger.error("node_error", node=node_name, error=str(e),
                     correlation_id=correlation_id)
        return {
            "answer": "죄송합니다. 답변 생성 중 오류가 발생했습니다.",
            "error": f"{node_name} 실패: {e}",
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }


def check_satisfaction(state: ProductionState) -> dict:
    """[노드 3] 만족도 확인 — 에러 상태면 무조건 satisfied=True (루프 방지)"""
    node_name = "check_satisfaction"
    correlation_id = state.get("correlation_id", "unknown")

    if state.get("error"):
        return {
            "satisfied": True,
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }

    try:
        answer = state.get("answer", "")
        user_message = state["messages"][-1].content

        response = _call_llm([
            SystemMessage(content="답변이 질문에 충분히 답하고 있으면 'yes', 그렇지 않으면 'no'만 출력하세요."),
            HumanMessage(content=f"질문: {user_message}\n답변: {answer}"),
        ])

        satisfied = response.content.strip().lower() == "yes"
        retry_count = state.get("retry_count", 0)

        logger.info("node_success", node=node_name, satisfied=satisfied,
                    retry_count=retry_count, correlation_id=correlation_id)

        return {
            "satisfied": satisfied,
            "retry_count": retry_count + (0 if satisfied else 1),
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }

    except Exception as e:
        logger.error("node_error", node=node_name, error=str(e),
                     correlation_id=correlation_id)
        return {
            "satisfied": True,
            "error": f"{node_name} 실패: {e}",
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }


def should_retry(state: ProductionState) -> str:
    """Conditional edge: 에러 상태면 무조건 종료"""
    if state.get("error"):
        return "end"
    satisfied = state.get("satisfied", True)
    retry_count = state.get("retry_count", 0)
    if satisfied or retry_count >= 2:
        return "end"
    return "generate_answer"
