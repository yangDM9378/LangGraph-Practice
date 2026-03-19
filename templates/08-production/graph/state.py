from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class ProductionState(TypedDict):
    messages: Annotated[list, add_messages]
    category: str
    answer: str
    satisfied: bool
    retry_count: int
    nodes_visited: list[str]
    # 프로덕션 추가 필드
    error: str          # 에러 발생 시 에러 메시지 저장
    correlation_id: str  # 요청 추적용 고유 ID
