from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class FAQState(TypedDict):
    # 대화 메시지 히스토리 - add_messages reducer로 자동 누적
    messages: Annotated[list, add_messages]
    # 질문 분류 결과 (기술지원 / 결제 / 배송 / 기타)
    category: str
    # 최종 생성된 답변
    answer: str
    # 답변 품질 만족 여부
    satisfied: bool
    # 재시도 횟수 (최대 2회)
    retry_count: int
    # 방문한 노드 목록 (UI에서 진행 상태 표시용)
    nodes_visited: list[str]
