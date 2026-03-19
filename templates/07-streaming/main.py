import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

# 06-memory의 graph 구조를 그대로 가져와 사용합니다
# from graph.graph import graph

app = FastAPI(title="Streaming Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    thread_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    SSE(Server-Sent Events)로 토큰 단위 스트리밍 응답을 제공합니다.

    클라이언트는 text/event-stream 형식으로 토큰을 하나씩 수신합니다.
    각 이벤트 형식: data: {"token": "..."}\n\n
    종료 신호:     data: [DONE]\n\n
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    config = {"configurable": {"thread_id": request.thread_id}}
    state = {"messages": [HumanMessage(content=request.message)]}

    async def generate():
        # TODO: graph.astream_events(state, config, version="v2")를 순회하며
        #       "on_chat_model_stream" 이벤트의 토큰을 SSE로 yield하세요
        #
        # 힌트:
        # async for event in graph.astream_events(state, config, version="v2"):
        #     if event["event"] == "on_chat_model_stream":
        #         chunk = event["data"]["chunk"]
        #         token = chunk.content
        #         if token:
        #             yield f"data: {json.dumps({'token': token})}\n\n"
        # yield "data: [DONE]\n\n"
        raise NotImplementedError("generate()를 구현해 주세요")

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # nginx 버퍼링 비활성화
        },
    )
