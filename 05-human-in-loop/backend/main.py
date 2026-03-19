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

    # interrupt()에서 중단되므로 현재 상태에서 draft_answer를 읽습니다
    await graph.ainvoke(initial_state, config=config)
    state = graph.get_state(config)
    draft = state.values.get("draft_answer", "")

    return DraftResponse(thread_id=thread_id, draft_answer=draft, status="pending_approval")


@app.post("/approve", response_model=FinalResponse)
async def approve(request: ApproveRequest):
    config = make_config(request.thread_id)
    result = await graph.ainvoke(Command(resume=request.decision), config=config)
    final = result.get("final_answer", "")
    return FinalResponse(thread_id=request.thread_id, final_answer=final, status="completed")
