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

    # TODO: 노드를 등록하세요
    # builder.add_node("supervisor", supervisor)
    # builder.add_node("research_agent", research_agent)
    # builder.add_node("writer_agent", writer_agent)

    # TODO: START → supervisor 엣지 추가

    # TODO: supervisor의 conditional edge 추가
    # route_by_next 함수로 next 값에 따라 분기
    # {"research_agent": "research_agent", "writer_agent": "writer_agent", "FINISH": END}

    # TODO: 각 agent → supervisor 복귀 엣지 추가

    raise NotImplementedError("graph.py를 완성해 주세요")

    return builder.compile()


graph = build_graph()
