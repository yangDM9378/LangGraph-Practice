from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from graph.state import MemoryBotState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)


def chat(state: MemoryBotState) -> dict:
    system = SystemMessage(content=(
        "당신은 친절한 고객 지원 챗봇입니다. "
        "이전 대화 내용을 기억하고 맥락에 맞게 답변하세요. "
        "한국어로 답변하세요."
    ))
    response = llm.invoke([system] + state["messages"])
    return {"messages": [response]}
