from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from graph.state import ToolBotState
from graph.nodes import agent
from graph.tools import tools


def build_graph():
    """
    도구를 사용하는 에이전트 그래프

    흐름:
    START → agent ──(tool_call 있음)──→ tools → agent
                  └──(tool_call 없음)──→ END

    핵심:
    - ToolNode: tool_call 메시지를 보고 도구를 자동 실행
    - tools_condition: 마지막 메시지에 tool_call 있으면 "tools", 없으면 END
    """
    builder = StateGraph(ToolBotState)

    # TODO: 노드를 등록하세요
    # builder.add_node("agent", agent)
    # builder.add_node("tools", ToolNode(tools))  ← ToolNode 등록

    # TODO: 엣지를 연결하세요
    # builder.add_edge(START, "agent")

    # TODO: tools_condition으로 조건부 엣지를 추가하세요
    # 힌트: builder.add_conditional_edges("agent", tools_condition)
    # tools_condition은 자동으로 {"tools": "tools", END: END}를 처리합니다

    # TODO: tools → agent 엣지를 추가하세요 (도구 실행 후 에이전트로 복귀)

    raise NotImplementedError("graph.py를 완성해 주세요")

    return builder.compile()


graph = build_graph()
