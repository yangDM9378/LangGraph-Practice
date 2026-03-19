from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

# Supervisor가 선택할 수 있는 작업자 목록
WORKERS = ["research_agent", "writer_agent"]
OPTIONS = WORKERS + ["FINISH"]


class MultiAgentState(TypedDict):
    # 전체 대화 히스토리
    messages: Annotated[list, add_messages]
    # Supervisor가 다음에 실행할 에이전트 이름 ("FINISH"면 종료)
    next: str
    # research_agent가 수집한 정보 (writer_agent가 사용)
    research_result: str
    # 방문한 노드 목록
    nodes_visited: list[str]
