from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import MultiAgentState, OPTIONS

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=64)

SUPERVISOR_PROMPT = """당신은 고객 지원 팀의 감독자입니다.
사용자 요청을 분석하고 다음에 누가 작업해야 할지 결정하세요.

작업자 목록:
- research_agent: FAQ, 상품 정보, 주문 정보를 수집합니다
- writer_agent: 수집된 정보로 최종 답변을 작성합니다
- FINISH: 모든 작업이 완료되어 답변할 준비가 됐을 때

반드시 다음 중 하나만 출력하세요: {options}
다른 말은 절대 하지 마세요."""


def supervisor(state: MultiAgentState) -> dict:
    """
    [Supervisor 노드]
    현재 상태를 보고 다음 작업자를 선택합니다.

    반환: {"next": "research_agent" | "writer_agent" | "FINISH"}
    """
    system = SystemMessage(content=SUPERVISOR_PROMPT.format(options=OPTIONS))
    messages = [system] + state["messages"]
    response = llm.invoke(messages)
    next_agent = response.content.strip()
    if next_agent not in OPTIONS:
        next_agent = "FINISH"
    return {
        "next": next_agent,
        "nodes_visited": state.get("nodes_visited", []) + ["supervisor"],
    }
