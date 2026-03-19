from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class LangSmithState(TypedDict):
    messages: Annotated[list, add_messages]
    category: str
    answer: str
    satisfied: bool
    retry_count: int
    nodes_visited: list[str]
    error: str
    correlation_id: str
    # LangSmith 추가 필드
    user_id: str        # 사용자 식별자 (메타데이터로 LangSmith에 전달)
    session_id: str     # 세션 식별자 (thread 단위 추적)
