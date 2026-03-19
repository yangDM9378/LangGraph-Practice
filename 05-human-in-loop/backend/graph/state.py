from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class HumanLoopState(TypedDict):
    messages: Annotated[list, add_messages]
    # 사람에게 검토받을 초안 답변
    draft_answer: str
    # 사람이 승인/수정한 최종 답변
    final_answer: str
    # 사람의 결정 ("approved" | "rejected" | 수정된 텍스트)
    human_decision: str
    nodes_visited: list[str]
