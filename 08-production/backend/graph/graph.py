from langgraph.graph import StateGraph, START, END
from graph.state import ProductionState
from graph.nodes import classify_question, generate_answer, check_satisfaction, should_retry


def build_graph():
    """01-faq-bot와 동일한 구조이나 nodes.py에 에러 핸들링이 추가됨"""
    builder = StateGraph(ProductionState)

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
