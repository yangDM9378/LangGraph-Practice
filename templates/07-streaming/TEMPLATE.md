# 07 · Streaming — astream_events, 실시간 응답

## 학습 목표

- [ ] `graph.astream_events()`로 그래프 이벤트를 스트리밍하는 방법 이해
- [ ] `on_chat_model_stream` 이벤트로 토큰 단위 스트리밍 구현
- [ ] FastAPI `StreamingResponse`로 SSE(Server-Sent Events) 전달
- [ ] 프론트엔드에서 `EventSource` 또는 `fetch + ReadableStream`으로 수신

## 핵심 개념

### astream_events
그래프 실행 중 발생하는 이벤트를 비동기 스트림으로 반환한다.

```python
async for event in graph.astream_events(state, config, version="v2"):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        chunk = event["data"]["chunk"]
        token = chunk.content
        yield f"data: {token}\n\n"  # SSE 포맷
```

### 주요 이벤트 타입

| 이벤트 | 발생 시점 |
|--------|-----------|
| `on_chain_start` | 그래프/노드 시작 |
| `on_chain_end` | 그래프/노드 종료 |
| `on_chat_model_start` | LLM 호출 시작 |
| `on_chat_model_stream` | 토큰 생성 중 |
| `on_chat_model_end` | LLM 호출 완료 |
| `on_tool_start` / `on_tool_end` | 도구 실행 |

### SSE (Server-Sent Events)
단방향 서버→클라이언트 스트리밍. WebSocket보다 단순하다.

```python
# FastAPI
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
async def stream(request: ChatRequest):
    async def generate():
        async for event in graph.astream_events(...):
            if event["event"] == "on_chat_model_stream":
                token = event["data"]["chunk"].content
                if token:
                    yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 프론트엔드 수신

```javascript
const response = await fetch('/chat/stream', { method: 'POST', ... });
const reader = response.body.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = new TextDecoder().decode(value);
    // SSE 파싱 → 토큰 추출 → 화면에 추가
}
```

## 뼈대 코드 구조

```
backend/
├── graph/           ← 06-memory와 유사한 단순 구조
├── main.py          ← /chat/stream 엔드포인트 추가
└── requirements.txt

frontend/src/
├── api/
│   └── stream.js    ← fetch 스트리밍 클라이언트  ← 핵심 추가
└── components/
    └── StreamingMessage.jsx  ← 타이핑 효과 컴포넌트
```

## TODO

`main.py`:
- [ ] `StreamingResponse` + `astream_events` 조합 구현
- [ ] `on_chat_model_stream` 이벤트에서 토큰 추출
- [ ] `[DONE]` 신호로 스트림 종료 알림

`frontend/api/stream.js`:
- [ ] `fetch` + `ReadableStream` 으로 SSE 수신
- [ ] 토큰을 받을 때마다 `onToken(token)` 콜백 호출

`frontend/components/StreamingMessage.jsx`:
- [ ] 토큰이 들어올 때마다 텍스트를 누적해 표시
- [ ] 스트리밍 중 커서 애니메이션 (|) 표시

## 체크포인트

```bash
# curl로 SSE 스트리밍 테스트
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "배송 정책을 알려줘", "thread_id": "test"}' \
  --no-buffer
# → 토큰이 하나씩 출력되는지 확인
```
