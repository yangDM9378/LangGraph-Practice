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

    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder.compile()


graph = build_graph()
