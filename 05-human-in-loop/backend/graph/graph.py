from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from graph.state import HumanLoopState
from graph.nodes import draft_answer, send_answer


def build_graph():
    """
    Human-in-the-Loop 그래프

    흐름:
    START → draft_answer ──[INTERRUPT: 사람 검토]──→ send_answer → END

    핵심: interrupt()가 있는 그래프는 반드시 checkpointer가 필요합니다.
    """
    builder = StateGraph(HumanLoopState)

    builder.add_node("draft_answer", draft_answer)
    builder.add_node("send_answer", send_answer)

    builder.add_edge(START, "draft_answer")
    builder.add_edge("draft_answer", "send_answer")
    builder.add_edge("send_answer", END)

    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


graph = build_graph()
