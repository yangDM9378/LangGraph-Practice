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

    # TODO: research_result와 user_message를 LLM에 제공해
    #       친절하고 명확한 최종 답변을 생성하세요
    # 결과는 messages에 AIMessage로 추가
    raise NotImplementedError("writer_agent를 구현해 주세요")
