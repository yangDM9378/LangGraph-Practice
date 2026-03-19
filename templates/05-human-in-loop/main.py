import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.types import Command

load_dotenv()

from graph.graph import graph  # noqa: E402

app = FastAPI(title="Human-in-the-Loop Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ApproveRequest(BaseModel):
    thread_id: str
    decision: str  # "approved" | "rejected" | 수정된 텍스트


class DraftResponse(BaseModel):
    thread_id: str
    draft_answer: str
    status: str  # "pending_approval"


class FinalResponse(BaseModel):
    thread_id: str
    final_answer: str
    status: str  # "completed"


def make_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=DraftResponse)
async def chat(request: ChatRequest):
    """
    대화를 시작합니다. 초안을 생성하고 사람의 검토를 기다립니다.
    thread_id를 반환하며, 이후 /approve에서 이 ID를 사용합니다.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    thread_id = str(uuid.uuid4())
    config = make_config(thread_id)

    initial_state = {
        "messages": [HumanMessage(content=request.message)],
        "draft_answer": "",
        "final_answer": "",
        "human_decision": "",
        "nodes_visited": [],
    }

    # TODO: graph.ainvoke(initial_state, config=config) 호출
    # interrupt()에서 중단되므로 GraphInterrupt 예외를 처리하거나
    # 중단 후 상태를 읽어 draft_answer를 반환하세요
    # 힌트: try/except로 GraphInterrupt를 잡거나,
    #       graph.get_state(config).values로 현재 상태를 읽으세요
    raise NotImplementedError("/chat 엔드포인트를 구현해 주세요")


@app.post("/approve", response_model=FinalResponse)
async def approve(request: ApproveRequest):
    """
    사람의 결정(승인/거부/수정)을 받아 그래프를 재개합니다.
    """
    config = make_config(request.thread_id)

    # TODO: Command(resume=request.decision)으로 그래프를 재개하세요
    # result = await graph.ainvoke(Command(resume=request.decision), config=config)
    raise NotImplementedError("/approve 엔드포인트를 구현해 주세요")
