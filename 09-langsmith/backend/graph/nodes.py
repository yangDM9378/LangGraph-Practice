import time
import structlog
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from tenacity import retry, stop_after_attempt, wait_exponential
from graph.state import LangSmithState

logger = structlog.get_logger()
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

CATEGORIES = ["기술지원", "결제", "배송", "기타"]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
def _call_llm(messages: list):
    return llm.invoke(messages)


# ── @traceable: 이 함수 호출이 LangSmith에 별도 span으로 기록됩니다 ──────
@traceable(name="classify_question", tags=["classification"])
def classify_question(state: LangSmithState) -> dict:
    """[노드 1] 질문 분류 — LangSmith @traceable 적용"""
    start = time.time()
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

        logger.info("node_success", node="classify_question", category=category,
                    latency_ms=round((time.time() - start) * 1000),
                    correlation_id=correlation_id)

        return {
            "category": category,
            "nodes_visited": state.get("nodes_visited", []) + ["classify_question"],
        }

    except Exception as e:
        logger.error("node_error", node="classify_question", error=str(e),
                     correlation_id=correlation_id)
        return {
            "category": "기타",
            "error": f"classify_question 실패: {e}",
            "nodes_visited": state.get("nodes_visited", []) + ["classify_question"],
        }


@traceable(name="generate_answer", tags=["generation"])
def generate_answer(state: LangSmithState) -> dict:
    """[노드 2] 답변 생성 — LangSmith @traceable 적용"""
    start = time.time()
    correlation_id = state.get("correlation_id", "unknown")

    if state.get("error"):
        return {
            "answer": "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "nodes_visited": state.get("nodes_visited", []) + ["generate_answer"],
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

        logger.info("node_success", node="generate_answer",
                    latency_ms=round((time.time() - start) * 1000),
                    correlation_id=correlation_id)

        return {
            "answer": response.content,
            "nodes_visited": state.get("nodes_visited", []) + ["generate_answer"],
        }

    except Exception as e:
        logger.error("node_error", node="generate_answer", error=str(e),
                     correlation_id=correlation_id)
        return {
            "answer": "죄송합니다. 답변 생성 중 오류가 발생했습니다.",
            "error": f"generate_answer 실패: {e}",
            "nodes_visited": state.get("nodes_visited", []) + ["generate_answer"],
        }


@traceable(name="check_satisfaction", tags=["evaluation"])
def check_satisfaction(state: LangSmithState) -> dict:
    """[노드 3] 만족도 확인 — LangSmith @traceable 적용"""
    correlation_id = state.get("correlation_id", "unknown")

    if state.get("error"):
        return {
            "satisfied": True,
            "nodes_visited": state.get("nodes_visited", []) + ["check_satisfaction"],
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

        logger.info("node_success", node="check_satisfaction", satisfied=satisfied,
                    retry_count=retry_count, correlation_id=correlation_id)

        return {
            "satisfied": satisfied,
            "retry_count": retry_count + (0 if satisfied else 1),
            "nodes_visited": state.get("nodes_visited", []) + ["check_satisfaction"],
        }

    except Exception as e:
        logger.error("node_error", node="check_satisfaction", error=str(e),
                     correlation_id=correlation_id)
        return {
            "satisfied": True,
            "error": f"check_satisfaction 실패: {e}",
            "nodes_visited": state.get("nodes_visited", []) + ["check_satisfaction"],
        }


def should_retry(state: LangSmithState) -> str:
    if state.get("error"):
        return "end"
    satisfied = state.get("satisfied", True)
    retry_count = state.get("retry_count", 0)
    if satisfied or retry_count >= 2:
        return "end"
    return "generate_answer"
