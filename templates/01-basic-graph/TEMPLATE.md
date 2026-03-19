# 01 · Basic Graph — StateGraph, Node, Conditional Edge

## 학습 목표

- [ ] `StateGraph`로 그래프를 정의하는 방법 이해
- [ ] `TypedDict`로 State를 설계하는 방법 이해
- [ ] 노드(함수)를 등록하고 엣지로 연결하는 방법 이해
- [ ] `add_conditional_edges`로 분기 로직 구현
- [ ] `add_messages` reducer의 역할 이해

## 핵심 개념

### State (상태)
그래프 전체가 공유하는 데이터 구조. 각 노드는 state의 일부를 **덮어쓰거나 누적**한다.

```python
class MyState(TypedDict):
    messages: Annotated[list, add_messages]  # reducer: 덮어쓰지 않고 누적
    result: str                               # 일반 필드: 덮어씀
```

### Node (노드)
`state`를 받아 **변경할 부분만 dict로 반환**하는 함수.

```python
def my_node(state: MyState) -> dict:
    # state를 읽어 처리
    return {"result": "처리 결과"}  # 변경된 필드만 반환
```

### Conditional Edge (조건부 엣지)
노드 실행 후 **다음 노드를 동적으로 결정**하는 함수.

```python
def router(state: MyState) -> str:
    if state["result"] == "ok":
        return "end"     # → END로 이동
    return "retry_node"  # → retry_node로 이동
```

## 구현할 그래프

```
START → classify_question → generate_answer → check_satisfaction
                                  ↑                   |
                                  └────(불만족, <2회)──┘
                                                       |
                                                (만족 or ≥2회)
                                                       ↓
                                                      END
```

## 뼈대 코드 구조

```
backend/
├── graph/
│   ├── __init__.py
│   ├── state.py      ← TypedDict State 정의
│   ├── nodes.py      ← 노드 함수 3개
│   └── graph.py      ← StateGraph 빌드
├── main.py           ← FastAPI 엔트리포인트
└── requirements.txt
```

## TODO (직접 채워야 할 부분)

`state.py`:
- [ ] `FAQState` TypedDict 필드 정의

`nodes.py`:
- [ ] `classify_question`: 질문을 카테고리로 분류
- [ ] `generate_answer`: 카테고리 기반 답변 생성
- [ ] `check_satisfaction`: 답변 품질 자체 평가
- [ ] `should_retry`: conditional edge 라우터

`graph.py`:
- [ ] `StateGraph(FAQState)` 생성
- [ ] 노드 3개 등록
- [ ] 엣지 연결
- [ ] `add_conditional_edges` 적용

## 완성 코드 참고
`01-faq-bot/backend/` 폴더를 참고하세요.
