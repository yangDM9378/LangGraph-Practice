from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from graph.tools import tools

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024)

SYSTEM_PROMPT = """당신은 고객 지원 에이전트입니다.
복잡한 질문에는 여러 도구를 단계적으로 사용해 답하세요.
한국어로 답변하세요.

사용 가능한 도구:
- search_faq: 정책/규정 검색
- calculate: 가격 계산
- get_product_info: 상품 정보 조회
"""

# ── 방법 1: create_react_agent 프리빌트 사용 ───────────────────────────
graph = create_react_agent(llm, tools=tools, state_modifier=SYSTEM_PROMPT)


# ── 방법 2: StateGraph 직접 구현 (참고용) ──────────────────────────────
# from langgraph.graph import StateGraph, START, END
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_core.messages import SystemMessage
# from graph.state import ReActState
#
# llm_with_tools = llm.bind_tools(tools)
#
# def agent(state: ReActState) -> dict:
#     system = SystemMessage(content=SYSTEM_PROMPT)
#     response = llm_with_tools.invoke([system] + state["messages"])
#     return {"messages": [response], "nodes_visited": state.get("nodes_visited", []) + ["agent"]}
#
# def build_graph():
#     builder = StateGraph(ReActState)
#     builder.add_node("agent", agent)
#     builder.add_node("tools", ToolNode(tools))
#     builder.add_edge(START, "agent")
#     builder.add_conditional_edges("agent", tools_condition)
#     builder.add_edge("tools", "agent")
#     return builder.compile()
#
# graph = build_graph()
