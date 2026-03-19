from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class MemoryBotState(TypedDict):
    # add_messages reducer 덕분에 Checkpointer가 저장한 이전 메시지 위에 새 메시지가 누적됨
    # 이것이 "대화 기억"의 핵심 메커니즘
    messages: Annotated[list, add_messages]
