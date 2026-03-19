from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langgraph.types import interrupt
from graph.state import HumanLoopState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)


def draft_answer(state: HumanLoopState) -> dict:
    """
    [노드 1] 초안 생성 + 사람 검토 요청

    LLM으로 초안을 생성한 뒤 interrupt()로 일시 중단합니다.
    UI는 초안을 보여주고 사람이 승인/거부/수정할 수 있습니다.
    """
    user_message = state["messages"][-1].content

    response = llm.invoke([
        SystemMessage(content="고객 지원 챗봇입니다. 초안 답변을 작성하세요. 한국어로 답변하세요."),
        *state["messages"],
    ])
    draft = response.content.strip()

    # TODO: interrupt()를 호출해 초안을 UI에 전달하고 일시 중단하세요
    # 힌트: human_decision = interrupt({"draft": draft, "question": "이 답변을 전송할까요?"})
    # interrupt()의 반환값이 나중에 Command(resume=...)로 전달한 값이 됩니다
    raise NotImplementedError("interrupt()를 추가해 주세요")

    return {
        "draft_answer": draft,
        "human_decision": human_decision,
        "nodes_visited": state.get("nodes_visited", []) + ["draft_answer"],
    }


def send_answer(state: HumanLoopState) -> dict:
    """
    [노드 2] 최종 답변 전송

    사람의 결정에 따라 초안을 그대로 사용하거나 수정합니다.
    """
    decision = state.get("human_decision", "approved")
    draft = state.get("draft_answer", "")

    # TODO: decision이 "approved"면 draft를 사용,
    #       "rejected"면 "답변이 취소됐습니다"를,
    #       그 외(수정된 텍스트)면 decision을 final_answer로 설정
    raise NotImplementedError("send_answer를 구현해 주세요")
