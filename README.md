# LangGraph Practice

LangGraph를 단계별로 학습하는 실습 프로젝트입니다.
기본 개념부터 프로덕션 수준까지 단계별로 실전 감각을 익히는 것이 목표입니다.

---

## 학습 로드맵

| 단계 | 폴더 | 핵심 개념 | 상태 |
|------|------|-----------|------|
| 01 | `01-faq-bot/` | StateGraph, Node, Conditional Edge | ✅ |
| 02 | `02-tool-use/` | @tool, ToolNode, bind_tools | ✅ |
| 03 | `03-react-agent/` | ReAct 패턴, create_react_agent | ✅ |
| 04 | `04-multi-agent/` | Supervisor 패턴, 서브에이전트 | ✅ |
| 05 | `05-human-in-loop/` | interrupt(), 사람 승인 흐름 | ✅ |
| 06 | `06-memory/` | Checkpointer, thread_id 기반 대화 기억 | ✅ |
| 07 | `07-streaming/` | astream_events, SSE | ✅ |
| 08 | `08-production/` | 에러 핸들링, 구조화 로깅, Retry | ✅ |
| 09 | `09-langsmith/` | LangSmith 트레이싱, @traceable, metadata | ✅ |

각 단계는 이전 단계 위에 **개념 하나**만 더합니다.

---

## 01 · Basic Graph (FAQ Bot)

LangGraph 기본 구조 학습. 질문 분류 → 답변 생성 → 만족도 확인 루프를 구현합니다.

```
START → classify → generate → check
                      ↑          |
                      └─(retry)──┘
                                 └→ END
```

| 항목 | 내용 |
|------|------|
| 배우는 것 | TypedDict State, 노드 함수, add_conditional_edges, 루프 |
| 핵심 포인트 | `add_messages` reducer, `should_retry` 조건 함수 |

---

## 02 · Tool Use

LLM이 도구 호출 여부를 직접 결정하는 에이전트를 구현합니다.

```
START → agent ──(tool_call?)──→ tools → agent
              └──(no tool)──→ END
```

| 항목 | 내용 |
|------|------|
| 배우는 것 | LangChain 도구 정의, LLM에 도구 바인딩, 자동 도구 실행 |
| 핵심 포인트 | `@tool`, `bind_tools`, `ToolNode`, `tools_condition` |

---

## 03 · ReAct Agent

추론-행동(Reason-Act) 루프로 복잡한 질문을 단계적으로 해결합니다.

```
START → agent ──(tool_call?)──→ tools → agent → ...→ END
```

| 항목 | 내용 |
|------|------|
| 배우는 것 | ReAct 패턴, 멀티툴 루프 |
| 핵심 포인트 | `create_react_agent` 프리빌트 활용 |

---

## 04 · Multi-Agent (Supervisor)

Supervisor가 여러 전문 에이전트를 조율하는 구조를 구현합니다.

```
START → supervisor ──→ research_agent ─┐
                  └──→ writer_agent   ─┴→ supervisor → END
```

| 항목 | 내용 |
|------|------|
| 배우는 것 | 여러 전문 에이전트 조율, 서브그래프 합성 |
| 핵심 포인트 | Supervisor가 `next` 필드로 다음 에이전트를 동적 선택 |

---

## 05 · Human-in-the-Loop

민감한 작업 전 사람이 검토·승인할 수 있는 구조를 구현합니다.

```
START → draft_answer → [INTERRUPT: 사람 검토] → send_answer → END
```

| 항목 | 내용 |
|------|------|
| 배우는 것 | 그래프 일시 중단, 사람 승인 후 재개 |
| 핵심 포인트 | `interrupt()`, `Command(resume=...)`, `MemorySaver` |

---

## 06 · Memory & Persistence

같은 `thread_id`로 반복 호출하면 이전 대화를 기억합니다.

```
thread_id="user-123" → [이전 메시지 복원] → 새 메시지 처리 → [저장]
```

| 항목 | 내용 |
|------|------|
| 배우는 것 | 세션 간 상태 지속, thread_id 기반 대화 기억 |
| 핵심 포인트 | `compile(checkpointer=checkpointer)`, `SqliteSaver` |

---

## 07 · Streaming

토큰을 생성하는 즉시 브라우저에 전달하는 실시간 응답을 구현합니다.

```
graph.astream_events() → yield token → SSE → 브라우저 실시간 렌더링
```

| 항목 | 내용 |
|------|------|
| 배우는 것 | 토큰 스트리밍, SSE(Server-Sent Events) |
| 핵심 포인트 | `astream_events`, FastAPI `StreamingResponse` |

---

## 08 · Production

실제 서비스 수준의 에러 핸들링과 구조화 로깅을 적용합니다.

| 항목 | 내용 |
|------|------|
| 배우는 것 | 노드별 try/except, 구조화 로깅, Rate Limit 대응 |
| 핵심 포인트 | `structlog`, `tenacity` retry, fallback 노드 |

---

## 09 · LangSmith

LangSmith로 그래프 실행을 실시간으로 모니터링합니다.

| 항목 | 내용 |
|------|------|
| 배우는 것 | 트레이스 시각화, 노드별 latency/토큰 확인 |
| 핵심 포인트 | `@traceable`, `ainvoke config` (run_name/tags/metadata), `LANGCHAIN_TRACING_V2=true` |

**필요한 환경 변수** (`.env`):
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_key
LANGCHAIN_PROJECT=langgraph-practice
```

---

## 공통 실행 방법

```bash
cd {단계폴더}/backend
python -m venv venv && source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env   # API 키 입력
uvicorn main:app --reload

cd ../frontend
npm install
npm run dev
```

---

## 사전 준비

- Python 3.11+
- Node.js 18+
- [Anthropic API Key](https://console.anthropic.com/)
- [LangSmith API Key](https://smith.langchain.com/) (09단계)

---

## 참고 자료

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain 공식 문서](https://python.langchain.com/)
- [LangSmith 공식 문서](https://docs.smith.langchain.com/)
