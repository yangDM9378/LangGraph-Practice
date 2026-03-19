from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class ToolBotState(TypedDict):
    # add_messages reducer: 새 메시지를 덮어쓰지 않고 리스트에 누적
    messages: Annotated[list, add_messages]
    # 방문한 노드 목록 (UI 표시용)
    nodes_visited: list[str]
