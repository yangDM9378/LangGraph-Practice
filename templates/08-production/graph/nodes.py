import time
import structlog
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from graph.state import ProductionState

logger = structlog.get_logger()
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

CATEGORIES = ["기술지원", "결제", "배송", "기타"]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    # TODO: retry_if_exception_type으로 Rate Limit 에러만 재시도하도록 설정
)
def _call_llm(messages: list) -> str:
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
            SystemMessage(content=(
                "질문을 분류하세요. 다음 중 하나만 출력: 기술지원, 결제, 배송, 기타"
            )),
            HumanMessage(content=user_message),
        ])

        category = response.content.strip()
        if category not in CATEGORIES:
            category = "기타"

        # TODO: structlog로 성공 로그를 남기세요
        # logger.info("node_success", node=node_name, category=category,
        #             latency_ms=round((time.time()-start)*1000),
        #             correlation_id=correlation_id)

        return {
            "category": category,
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }

    except Exception as e:
        # TODO: structlog로 에러 로그를 남기고 error 필드를 반환하세요
        # logger.error("node_error", node=node_name, error=str(e), ...)
        return {
            "category": "기타",
            "error": f"{node_name} 실패: {e}",
            "nodes_visited": state.get("nodes_visited", []) + [node_name],
        }


def generate_answer(state: ProductionState) -> dict:
    """[노드 2] 답변 생성 — 에러 상태 확인 후 처리"""
    # TODO: state에 error가 있으면 fallback 메시지를 반환하세요
    # 이미 에러가 났다면 LLM을 다시 호출할 필요 없음

    # TODO: 정상 경로: 01-faq-bot의 generate_answer와 동일하게 구현
    #       + try/except + 구조화 로깅 추가
    raise NotImplementedError("generate_answer를 구현해 주세요")


def check_satisfaction(state: ProductionState) -> dict:
    """[노드 3] 만족도 확인 — 에러 상태면 무조건 satisfied=True (루프 방지)"""
    # TODO: error가 있으면 satisfied=True로 즉시 반환 (무한 루프 방지)
    # TODO: 정상 경로: 01-faq-bot의 check_satisfaction + try/except + 로깅
    raise NotImplementedError("check_satisfaction을 구현해 주세요")


def should_retry(state: ProductionState) -> str:
    """Conditional edge: 에러 상태면 무조건 종료"""
    if state.get("error"):
        return "end"
    satisfied = state.get("satisfied", True)
    retry_count = state.get("retry_count", 0)
    if satisfied or retry_count >= 2:
        return "end"
    return "generate_answer"
