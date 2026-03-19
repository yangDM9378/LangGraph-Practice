# 05 · Human-in-the-Loop — interrupt(), 승인 흐름

## 학습 목표

- [ ] `interrupt()`로 그래프를 일시 중단하는 방법 이해
- [ ] `Command(resume=value)`로 그래프를 재개하는 방법 이해
- [ ] `MemorySaver`로 중단 상태를 보존하는 방법 이해
- [ ] 사람의 승인이 필요한 작업(민감한 답변, 환불 처리 등)에 적용

## 핵심 개념

### interrupt()
노드 실행 중에 호출하면 그래프가 **즉시 일시 중단**된다.
값을 전달해 UI에 "무엇을 승인해야 하는지" 알릴 수 있다.

```python
from langgraph.types import interrupt

def review_answer(state):
    draft = generate_draft(state)
    # 여기서 일시 중단 → 사람이 승인/수정 가능
    human_decision = interrupt({
        "draft_answer": draft,
        "message": "이 답변을 전송해도 될까요?"
    })
    return {"final_answer": human_decision or draft}
```

### Command(resume=value)
중단된 그래프를 재개할 때 사용. `value`가 `interrupt()`의 반환값이 된다.

```python
from langgraph.types import Command

# 사람이 "승인"을 클릭하면 서버에서:
graph.invoke(Command(resume="approved"), config=thread_config)
```

### MemorySaver (필수)
interrupt를 사용하려면 반드시 checkpointer가 필요하다.
중단 상태를 저장해야 나중에 재개할 수 있기 때문.

```python
from langgraph.checkpoint.memory import MemorySaver
graph = builder.compile(checkpointer=MemorySaver())
```

## 구현할 흐름

```
POST /chat   →  draft_answer 생성  →  [INTERRUPT]
                                           ↓
                               UI에 초안 표시 + 승인 버튼
                                           ↓
POST /approve  →  Command(resume="approved")  →  send_answer  →  END
```

## API 설계

```
POST /chat           → 그래프 시작, 초안 반환 + thread_id
POST /approve        → thread_id + 결정(approved/rejected) 전달, 재개
GET  /status/{id}    → 현재 그래프 상태 확인
```

## 뼈대 코드 구조

```
backend/
├── graph/
│   ├── __init__.py
│   ├── state.py      ← draft_answer, final_answer 필드 추가
│   ├── nodes.py      ← draft_node (interrupt 포함), send_node
│   └── graph.py      ← MemorySaver 필수
├── main.py           ← /chat, /approve, /status 엔드포인트
└── requirements.txt
```

## TODO

`nodes.py`:
- [ ] `draft_answer`: 초안을 생성하고 `interrupt()` 호출
- [ ] `send_answer`: 승인된 답변을 최종 반환

`graph.py`:
- [ ] `MemorySaver()` checkpointer 연결
- [ ] `compile(checkpointer=checkpointer)` 적용

`main.py`:
- [ ] `thread_id`를 UUID로 생성하고 config에 전달
- [ ] `/approve` 엔드포인트에서 `Command(resume=...)` 전달

## 체크포인트

```python
# 1단계: 초안 생성 (중단됨)
result = graph.invoke(initial_state, config={"configurable": {"thread_id": "abc"}})
# → GraphInterrupt 예외 또는 중단 상태 반환

# 2단계: 승인 후 재개
from langgraph.types import Command
result = graph.invoke(Command(resume="approved"), config={"configurable": {"thread_id": "abc"}})
```
