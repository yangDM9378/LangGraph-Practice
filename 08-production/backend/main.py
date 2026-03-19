import uuid
import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

from graph.graph import graph  # noqa: E402

logger = structlog.get_logger()

app = FastAPI(title="Production FAQ Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """예상치 못한 에러를 잡아 500 응답으로 변환합니다."""
    logger.error("unhandled_exception",
                 path=request.url.path,
                 method=request.method,
                 error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요."},
    )


class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("메시지를 입력해주세요.")
        if len(v) > 1000:
            raise ValueError("메시지는 1000자를 초과할 수 없습니다.")
        return v


class ChatResponse(BaseModel):
    answer: str
    category: str
    nodes_visited: list[str]
    retry_count: int
    correlation_id: str
    error: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    correlation_id = str(uuid.uuid4())

    logger.info("request_received",
                correlation_id=correlation_id,
                message_length=len(request.message))

    initial_state = {
        "messages": [HumanMessage(content=request.message)],
        "category": "",
        "answer": "",
        "satisfied": False,
        "retry_count": 0,
        "nodes_visited": [],
        "error": "",
        "correlation_id": correlation_id,
    }

    result = await graph.ainvoke(initial_state)

    logger.info("request_completed",
                correlation_id=correlation_id,
                category=result["category"],
                retry_count=result["retry_count"],
                nodes=result["nodes_visited"],
                has_error=bool(result.get("error")))

    return ChatResponse(
        answer=result["answer"] or "답변을 생성하지 못했습니다.",
        category=result["category"],
        nodes_visited=result["nodes_visited"],
        retry_count=result["retry_count"],
        correlation_id=correlation_id,
        error=result.get("error") or None,
    )
