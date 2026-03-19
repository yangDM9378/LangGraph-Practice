from langgraph.graph import StateGraph, START, END
from graph.state import MemoryBotState
from graph.nodes import chat


async def build_graph(checkpointer):
    builder = StateGraph(MemoryBotState)
    builder.add_node("chat", chat)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)
    return builder.compile(checkpointer=checkpointer)
