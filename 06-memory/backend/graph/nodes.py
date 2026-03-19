from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from graph.state import MemoryBotState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)


def chat(state: MemoryBotState) -> dict:
    """
    [대화 노드]
    전체 메시지 히스토리를 보고 답변합니다.
    Checkpointer가 이전 대화를 state["messages"]에 자동으로 복원합니다.
    """
    system = SystemMessage(content=(
        "당신은 친절한 고객 지원 챗봇입니다. "
        "이전 대화 내용을 기억하고 맥락에 맞게 답변하세요. "
        "한국어로 답변하세요."
    ))

    # state["messages"]에는 이전 대화 + 현재 메시지가 모두 포함됨
    response = llm.invoke([system] + state["messages"])

    return {"messages": [response]}
