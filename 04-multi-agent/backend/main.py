from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

from graph.graph import graph  # noqa: E402

app = FastAPI(title="Multi-Agent API")

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
    nodes_visited: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    initial_state = {
        "messages": [HumanMessage(content=request.message)],
        "next": "",
        "research_result": "",
        "nodes_visited": [],
    }

    result = await graph.ainvoke(initial_state)

    ai_messages = [
        m for m in result["messages"]
        if hasattr(m, "content") and not hasattr(m, "tool_call_id")
        and not isinstance(m, HumanMessage)
    ]
    answer = ai_messages[-1].content if ai_messages else "답변을 생성하지 못했습니다."

    return ChatResponse(
        answer=answer,
        nodes_visited=result.get("nodes_visited", []),
    )
