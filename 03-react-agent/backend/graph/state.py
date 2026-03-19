from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class ReActState(TypedDict):
    messages: Annotated[list, add_messages]
    nodes_visited: list[str]
    # ReAct에서는 추론 단계를 messages 안에 모두 담는다
    # tool_call → ToolMessage → AIMessage 순서로 쌓임
