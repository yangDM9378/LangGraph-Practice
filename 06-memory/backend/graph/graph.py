from langgraph.graph import StateGraph, START, END
from graph.state import MemoryBotState
from graph.nodes import chat


async def build_graph(checkpointer):
    """
    Memory Bot 그래프

    핵심: compile(checkpointer=checkpointer)
    같은 thread_id로 호출하면 Checkpointer가 이전 상태를 복원한다.

    흐름: START → chat → END
    """
    builder = StateGraph(MemoryBotState)
    builder.add_node("chat", chat)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)

    return builder.compile(checkpointer=checkpointer)
