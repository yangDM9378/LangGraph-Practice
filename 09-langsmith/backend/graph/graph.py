from langgraph.graph import StateGraph, START, END
from graph.state import LangSmithState
from graph.nodes import classify_question, generate_answer, check_satisfaction, should_retry


def build_graph():
    """
    LangSmith 트레이싱이 적용된 그래프

    핵심:
    - LANGCHAIN_TRACING_V2=true 환경 변수만으로 자동 트레이싱
    - @traceable 데코레이터로 노드별 상세 span 기록
    - graph.ainvoke(..., config={"metadata": {...}}) 로 메타데이터 전달

    흐름:
    START → classify → generate → check
                           ↑          |
                           └─(retry)──┘
                                      └→ END
    """
    builder = StateGraph(LangSmithState)

    builder.add_node("classify_question", classify_question)
    builder.add_node("generate_answer", generate_answer)
    builder.add_node("check_satisfaction", check_satisfaction)

    builder.add_edge(START, "classify_question")
    builder.add_edge("classify_question", "generate_answer")
    builder.add_edge("generate_answer", "check_satisfaction")
    builder.add_conditional_edges(
        "check_satisfaction",
        should_retry,
        {"end": END, "generate_answer": "generate_answer"},
    )

    return builder.compile()


graph = build_graph()
