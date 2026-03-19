from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import FAQState

# 비용 최소화를 위해 Haiku 사용
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

CATEGORIES = ["기술지원", "결제", "배송", "기타"]


def classify_question(state: FAQState) -> dict:
    """
    [노드 1] 질문 분류
    사용자 질문을 4개 카테고리 중 하나로 분류합니다.
    """
    user_message = state["messages"][-1].content

    response = llm.invoke([
        SystemMessage(content=(
            "당신은 고객 문의를 분류하는 전문가입니다. "
            "다음 카테고리 중 하나만 답하세요: 기술지원, 결제, 배송, 기타\n"
            "카테고리 이름만 정확히 출력하세요. 다른 말은 하지 마세요."
        )),
        HumanMessage(content=user_message),
    ])

    category = response.content.strip()
    if category not in CATEGORIES:
        category = "기타"

    return {
        "category": category,
        "nodes_visited": state.get("nodes_visited", []) + ["classify_question"],
    }


def generate_answer(state: FAQState) -> dict:
    """
    [노드 2] 답변 생성
    분류된 카테고리를 바탕으로 맞춤형 답변을 생성합니다.
    """
    user_message = state["messages"][-1].content
    category = state.get("category", "기타")
    retry_count = state.get("retry_count", 0)

    category_context = {
        "기술지원": "기술적인 문제 해결 전문가로서 단계별로 명확하게 안내해주세요.",
        "결제": "결제 및 환불 전문가로서 정책과 절차를 친절하게 설명해주세요.",
        "배송": "배송 및 물류 전문가로서 배송 현황과 예상 일정을 안내해주세요.",
        "기타": "고객 서비스 전문가로서 친절하고 도움이 되는 답변을 제공해주세요.",
    }

    retry_instruction = ""
    if retry_count > 0:
        retry_instruction = f"\n이전 답변이 불충분했습니다. 더 구체적이고 상세한 답변을 제공해주세요. (재시도 {retry_count}회)"

    response = llm.invoke([
        SystemMessage(content=(
            f"당신은 고객 지원 챗봇입니다. 카테고리: {category}\n"
            f"{category_context.get(category, '')}"
            f"{retry_instruction}\n"
            "한국어로 2-3문장 이내로 간결하게 답변하세요."
        )),
        HumanMessage(content=user_message),
    ])

    answer = response.content.strip()

    return {
        "answer": answer,
        "retry_count": retry_count,
        "nodes_visited": state.get("nodes_visited", []) + ["generate_answer"],
    }


def check_satisfaction(state: FAQState) -> dict:
    """
    [노드 3] 만족도 확인
    생성된 답변이 충분한지 자체 평가합니다.
    conditional edge에서 이 결과를 보고 루프 여부를 결정합니다.
    """
    user_message = state["messages"][-1].content
    answer = state.get("answer", "")
    retry_count = state.get("retry_count", 0)

    response = llm.invoke([
        SystemMessage(content=(
            "당신은 고객 답변 품질 평가자입니다.\n"
            "다음 질문과 답변을 보고 답변이 충분한지 평가하세요.\n"
            "답변이 충분하면 'YES', 불충분하면 'NO'만 출력하세요.\n\n"
            "평가 기준:\n"
            "- 질문에 직접적으로 답하고 있는가?\n"
            "- 실용적인 정보가 포함되어 있는가?\n"
            "- 너무 짧거나 모호하지 않은가?"
        )),
        HumanMessage(content=f"질문: {user_message}\n\n답변: {answer}"),
    ])

    satisfied = response.content.strip().upper() == "YES"

    return {
        "satisfied": satisfied,
        "retry_count": retry_count + (0 if satisfied else 1),
        "nodes_visited": state.get("nodes_visited", []) + ["check_satisfaction"],
    }


def should_retry(state: FAQState) -> str:
    """
    [Conditional Edge 함수]
    만족도 결과와 재시도 횟수를 보고 다음 노드를 결정합니다.

    반환값:
    - "end"           : 만족하거나 재시도 2회 초과 시 종료
    - "generate_answer": 불만족 시 답변 재생성 루프
    """
    satisfied = state.get("satisfied", True)
    retry_count = state.get("retry_count", 0)

    if satisfied or retry_count >= 2:
        return "end"
    return "generate_answer"
