from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from graph.graph import build_graph

load_dotenv()

graph = None  # lifespan에서 채울 예정


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 시작 시 DB 연결 + 그래프 초기화, 종료 시 정리"""
    global graph
    async with AsyncSqliteSaver.from_conn_string("chat.db") as checkpointer:
        graph = await build_graph(checkpointer)
        yield


app = FastAPI(title="Memory Bot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    thread_id: str  # 사용자/세션 식별자 (같은 ID면 대화 기억)


class ChatResponse(BaseModel):
    answer: str
    thread_id: str


class HistoryResponse(BaseModel):
    thread_id: str
    messages: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    config = {"configurable": {"thread_id": request.thread_id}}
    state = {"messages": [HumanMessage(content=request.message)]}

    result = await graph.ainvoke(state, config=config)

    answer = result["messages"][-1].content
    return ChatResponse(answer=answer, thread_id=request.thread_id)


@app.get("/history/{thread_id}", response_model=HistoryResponse)
async def get_history(thread_id: str):
    """특정 thread_id의 전체 대화 히스토리를 반환합니다."""
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)
    messages = [
        {"role": "human" if m.__class__.__name__ == "HumanMessage" else "ai", "content": m.content}
        for m in state.values.get("messages", [])
    ]
    return HistoryResponse(thread_id=thread_id, messages=messages)
