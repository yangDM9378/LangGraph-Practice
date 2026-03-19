from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage
from graph.state import MultiAgentState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

FAQ_DB = {
    "배송비": "기본 배송비 3,000원, 5만원 이상 무료 배송.",
    "환불": "구매 후 7일 이내 환불 가능.",
    "교환": "수령 후 3일 이내 교환 가능.",
}

PRODUCT_DB = {
    "노트북": "가격: 1,200,000원 / 재고: 있음 / 배송: 2일",
    "마우스": "가격: 35,000원 / 재고: 있음 / 배송: 1일",
    "키보드": "가격: 80,000원 / 재고: 품절",
}


def research_agent(state: MultiAgentState) -> dict:
    """
    [Research Agent 노드]
    사용자 질문에서 필요한 정보를 수집합니다.
    FAQ와 상품 DB를 검색하여 research_result에 저장합니다.
    """
    user_message = state["messages"][0].content

    # TODO: LLM을 사용해 user_message에서 검색 키워드를 추출하고
    #       FAQ_DB와 PRODUCT_DB에서 관련 정보를 수집하세요
    # 결과는 research_result에 문자열로 저장
    # 예: "FAQ - 배송비: ...\n상품 - 노트북: ..."
    raise NotImplementedError("research_agent를 구현해 주세요")
