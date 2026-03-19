from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

from graph.graph import graph  # noqa: E402

app = FastAPI(title="ReAct Agent API")

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
    tool_calls_made: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    result = await graph.ainvoke({"messages": [HumanMessage(content=request.message)]})

    ai_messages = [
        m for m in result["messages"]
        if hasattr(m, "content") and not hasattr(m, "tool_call_id")
    ]
    answer = ai_messages[-1].content if ai_messages else "답변을 생성하지 못했습니다."

    tool_calls_made = sum(
        1 for m in result["messages"] if hasattr(m, "tool_call_id")
    )

    return ChatResponse(answer=answer, tool_calls_made=tool_calls_made)
