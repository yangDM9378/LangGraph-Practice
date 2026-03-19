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
    # TODO: LLM에게 현재 상태와 작업자 목록을 제공하고
    #       다음 작업자 이름을 파싱해 반환하세요
    # 힌트:
    # 1. SUPERVISOR_PROMPT.format(options=OPTIONS)으로 시스템 메시지 구성
    # 2. state["messages"]를 함께 전달
    # 3. 응답 텍스트를 strip()하고 OPTIONS에 없으면 "FINISH" 처리
    raise NotImplementedError("supervisor를 구현해 주세요")
