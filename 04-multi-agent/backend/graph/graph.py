from langgraph.graph import StateGraph, START, END
from graph.state import MultiAgentState
from graph.supervisor import supervisor
from graph.agents.research import research_agent
from graph.agents.writer import writer_agent


def route_by_next(state: MultiAgentState) -> str:
    """Supervisor의 결정에 따라 다음 노드를 반환합니다."""
    return state["next"]


def build_graph():
    """
    Multi-Agent Supervisor 그래프

    흐름:
    START → supervisor → (next에 따라) → research_agent or writer_agent or END
                    ↑                              |
                    └──────────────────────────────┘
    """
    builder = StateGraph(MultiAgentState)

    builder.add_node("supervisor", supervisor)
    builder.add_node("research_agent", research_agent)
    builder.add_node("writer_agent", writer_agent)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges("supervisor", route_by_next, {
        "research_agent": "research_agent",
        "writer_agent": "writer_agent",
        "FINISH": END,
    })
    builder.add_edge("research_agent", "supervisor")
    builder.add_edge("writer_agent", "supervisor")

    return builder.compile()


graph = build_graph()
