from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graph.state import MultiAgentState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)


def writer_agent(state: MultiAgentState) -> dict:
    """
    [Writer Agent 노드]
    research_result를 바탕으로 사용자에게 전달할 최종 답변을 작성합니다.
    """
    user_message = state["messages"][0].content
    research_result = state.get("research_result", "수집된 정보 없음")

    system = SystemMessage(content="당신은 고객 지원 담당자입니다. 수집된 정보를 바탕으로 친절하고 명확하게 한국어로 답변하세요.")
    prompt = HumanMessage(content=f"사용자 질문: {user_message}\n\n수집된 정보:\n{research_result}")
    response = llm.invoke([system, prompt])
    return {
        "messages": [AIMessage(content=response.content)],
        "nodes_visited": state.get("nodes_visited", []) + ["writer_agent"],
    }
