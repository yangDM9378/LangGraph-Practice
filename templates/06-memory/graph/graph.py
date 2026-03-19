from langgraph.graph import StateGraph, START, END
from graph.state import MemoryBotState
from graph.nodes import chat


async def build_graph():
    """
    Memory Bot 그래프

    핵심: compile(checkpointer=checkpointer)
    같은 thread_id로 호출하면 Checkpointer가 이전 상태를 복원한다.

    흐름: START → chat → END
    단순한 흐름이지만, Checkpointer가 있으면 대화 기억이 가능해진다.
    """
    # TODO: AsyncSqliteSaver를 사용해 "chat.db"에 연결하세요
    # 힌트:
    # from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
    # checkpointer = AsyncSqliteSaver.from_conn_string("chat.db")
    # → 단, async context manager이므로 main.py에서 관리하는 게 좋습니다

    builder = StateGraph(MemoryBotState)
    builder.add_node("chat", chat)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)

    # TODO: checkpointer를 연결하세요
    # return builder.compile(checkpointer=checkpointer)
    raise NotImplementedError("checkpointer를 연결해 주세요")
