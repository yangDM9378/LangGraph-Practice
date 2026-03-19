from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from graph.state import ToolBotState
from graph.tools import tools

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

# TODO: llm에 tools를 바인딩하세요
# 힌트: llm.bind_tools(tools)
llm_with_tools = None  # ← 여기를 채우세요


def agent(state: ToolBotState) -> dict:
    """
    [에이전트 노드]
    메시지 히스토리를 보고 답변하거나 도구 호출을 결정합니다.
    LLM이 tool_call을 포함한 응답을 반환하면 ToolNode가 이어받아 실행합니다.
    """
    system = SystemMessage(content=(
        "당신은 고객 지원 챗봇입니다. "
        "FAQ 검색과 주문 조회 도구를 활용해 정확한 답변을 제공하세요. "
        "도구를 사용할 수 있으면 반드시 사용하세요. "
        "한국어로 답변하세요."
    ))
    messages = [system] + state["messages"]

    # TODO: llm_with_tools를 호출하고 결과를 반환하세요
    # 힌트: response = llm_with_tools.invoke(messages)
    # 반환: {"messages": [response], "nodes_visited": ...}
    raise NotImplementedError("agent 노드를 구현해 주세요")
