# 06 · Memory & Persistence — Checkpointer, 대화 기억

## 학습 목표

- [ ] `MemorySaver`와 `SqliteSaver`의 차이 이해
- [ ] `thread_id`로 대화 세션을 구분하는 방법 이해
- [ ] 같은 thread_id로 호출 시 이전 대화가 자동 복원되는 원리 파악
- [ ] `graph.get_state(config)`, `graph.get_state_history(config)` 활용

## 핵심 개념

### Checkpointer
그래프 실행 시점마다 상태를 저장하는 컴포넌트.
`thread_id`가 같으면 이전 상태 위에 새 상태를 쌓는다.

```python
# 인메모리 (재시작 시 초기화)
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()

# SQLite (디스크 저장, 재시작해도 유지)
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
async with AsyncSqliteSaver.from_conn_string("chat.db") as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
```

### thread_id
대화 세션을 구분하는 키. 같은 thread_id면 이전 메시지를 기억한다.

```python
config = {"configurable": {"thread_id": "user-123"}}
graph.invoke({"messages": [HumanMessage("안녕")]}, config=config)
graph.invoke({"messages": [HumanMessage("내 이름 기억해?")]}, config=config)
# → "네, 안녕하세요라고 하셨죠" (이전 대화 기억)
```

### 상태 조회

```python
# 현재 상태 스냅샷
state = graph.get_state(config)
print(state.values["messages"])

# 전체 히스토리 (체크포인트 목록)
for snapshot in graph.get_state_history(config):
    print(snapshot.metadata["step"], snapshot.values)
```

## 구현할 흐름

```
사용자 A (thread: user-123)
  1번 대화: "내 이름은 홍길동이야"
  2번 대화: "내 이름이 뭐야?" → "홍길동이세요"  ← 기억!

사용자 B (thread: user-456)
  1번 대화: "내 이름이 뭐야?" → "이름을 알려주지 않으셨어요"  ← 독립!
```

## 뼈대 코드 구조

```
backend/
├── graph/
│   ├── __init__.py
│   ├── state.py      ← 01과 동일 (messages + add_messages가 핵심)
│   ├── nodes.py      ← 단순 대화 노드
│   └── graph.py      ← SqliteSaver 연결
├── main.py           ← thread_id를 요청에서 받음
├── chat.db           ← SQLite DB (자동 생성)
└── requirements.txt  ← langgraph-checkpoint-sqlite 추가
```

## TODO

`graph.py`:
- [ ] `AsyncSqliteSaver`로 `chat.db`에 상태를 저장하세요
- [ ] `compile(checkpointer=checkpointer)` 적용

`main.py`:
- [ ] `ChatRequest`에 `thread_id: str` 필드 추가
- [ ] config에 thread_id 전달: `{"configurable": {"thread_id": thread_id}}`
- [ ] `/history/{thread_id}` 엔드포인트로 대화 히스토리 조회

## 체크포인트

```bash
# 서버 재시작 후에도 이전 대화를 기억하는지 확인
# 1번 요청: thread_id="test", message="내 이름은 Bob이야"
# 서버 재시작
# 2번 요청: thread_id="test", message="내 이름이 뭐야?"
# 예상: "Bob이라고 하셨습니다"
```

## 주의사항

- `MemorySaver`: 개발/테스트용. 서버 재시작 시 초기화됨.
- `SqliteSaver`: 파일에 저장. 프로덕션에선 PostgreSQL 사용 권장.
- thread_id 없이 호출하면 매번 새 대화로 취급됨.
