from langgraph.graph import StateGraph, START, END
from graph.state import FAQState
from graph.nodes import classify_question, generate_answer, check_satisfaction, should_retry


def build_graph():
    """
    LangGraph StateGraph 빌드

    흐름:
    START → classify_question → generate_answer → check_satisfaction
                                       ↑                   |
                                       └── (불만족, <2회) ──┘
                                                           |
                                                    (만족 or ≥2회)
                                                           ↓
                                                          END
    """
    builder = StateGraph(FAQState)

    # 노드 등록
    builder.add_node("classify_question", classify_question)
    builder.add_node("generate_answer", generate_answer)
    builder.add_node("check_satisfaction", check_satisfaction)

    # 엣지 연결
    builder.add_edge(START, "classify_question")
    builder.add_edge("classify_question", "generate_answer")
    builder.add_edge("generate_answer", "check_satisfaction")

    # Conditional Edge: check_satisfaction 결과에 따라 분기
    builder.add_conditional_edges(
        "check_satisfaction",
        should_retry,
        {
            "end": END,
            "generate_answer": "generate_answer",  # 루프백
        },
    )

    return builder.compile()


# 모듈 로드 시 한 번만 빌드
graph = build_graph()
