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
    checkpointer가 없으면 중단 상태를 저장할 수 없어 재개가 불가능합니다.
    """
    builder = StateGraph(HumanLoopState)

    # TODO: 노드 등록
    # TODO: 엣지 연결 (START → draft_answer → send_answer → END)

    # 반드시 MemorySaver 연결!
    checkpointer = MemorySaver()

    # TODO: builder.compile(checkpointer=checkpointer) 반환
    raise NotImplementedError("graph.py를 완성해 주세요")


graph = build_graph()
