# LangGraph Practice

LangGraph를 단계별로 학습하는 실습 프로젝트입니다.
기본 개념부터 프로덕션 수준까지 단계별로 실전 감각을 익히는 것이 목표입니다.

---

## 학습 로드맵

| 단계 | 폴더 | 핵심 개념 | 상태 |
|------|------|-----------|------|
| 01 | `01-faq-bot/` | StateGraph, Node, Conditional Edge | ✅ 완성 |
| 02 | `02-tool-use/` | @tool, ToolNode, bind_tools | ⬜ |
| 03 | `03-react-agent/` | ReAct 패턴, 검색/계산기 도구 | ⬜ |
| 04 | `04-multi-agent/` | Supervisor 패턴, 서브그래프 | ⬜ |
| 05 | `05-human-in-loop/` | interrupt(), 사람 승인 흐름 | ⬜ |
| 06 | `06-memory/` | Checkpointer, 대화 기억 | ⬜ |
| 07 | `07-streaming/` | astream_events, SSE | ⬜ |
| 08 | `08-production/` | 에러 핸들링, 구조화 로깅, Retry | ⬜ |
| 09 | `09-langsmith/` | LangSmith 트레이싱, @traceable, metadata | ⬜ |

각 단계는 이전 단계 위에 **개념 하나**만 더합니다.

---

## 01 · Basic Graph (FAQ Bot)

LangGraph의 기본 구조를 익히는 첫 번째 실습입니다.
사용자 질문을 분류 → 답변 생성 → 만족도 확인 → (불만족 시 재시도) 하는 FAQ 챗봇을 구현합니다.

### 그래프 흐름

```
START → classify → generate → check
                      ↑          |
                      └─(retry)──┘
                                 └→ END
```

### 기술 스택

- **Backend**: Python, FastAPI, LangGraph, LangChain
- **Frontend**: React, Vite
- **모델**: Claude Haiku (`claude-haiku-4-5-20251001`)

### 핵심 파일

```
01-faq-bot/
├── backend/
│   ├── graph/
│   │   ├── state.py      # FAQState (TypedDict)
│   │   ├── nodes.py      # classify_question, generate_answer, check_satisfaction
│   │   └── graph.py      # StateGraph 조립 + conditional edge
│   ├── main.py           # FastAPI POST /chat
│   └── requirements.txt
└── frontend/
    └── src/
        └── App.jsx       # 채팅 UI
```

### 실행 방법

**Backend**
```bash
cd 01-faq-bot/backend
python -m venv venv && source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env   # ANTHROPIC_API_KEY 입력
uvicorn main:app --reload
```

**Frontend**
```bash
cd 01-faq-bot/frontend
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
