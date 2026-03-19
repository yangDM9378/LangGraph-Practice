from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

from graph.graph import graph  # noqa: E402 (load_dotenv 먼저 실행 필요)

app = FastAPI(title="FAQ Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    category: str
    nodes_visited: list[str]
    retry_count: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    initial_state = {
        "messages": [HumanMessage(content=request.message)],
        "category": "",
        "answer": "",
        "satisfied": False,
        "retry_count": 0,
        "nodes_visited": [],
    }

    result = await graph.ainvoke(initial_state)

    return ChatResponse(
        answer=result["answer"],
        category=result["category"],
        nodes_visited=result["nodes_visited"],
        retry_count=result["retry_count"],
    )
