# 04 · Multi-Agent — Supervisor 패턴

## 학습 목표

- [ ] Supervisor가 여러 전문 에이전트를 조율하는 패턴 이해
- [ ] 서브그래프(subgraph)를 만들고 메인 그래프에 합성
- [ ] 에이전트 간 상태(State) 전달 방식 파악
- [ ] FINISH 조건으로 전체 작업 종료 시점 결정

## 핵심 개념

### Supervisor 패턴
하나의 "감독자" 에이전트가 여러 "전문가" 에이전트에게 작업을 위임한다.

```
사용자 질문
    ↓
Supervisor: "이 질문은 research_agent가 먼저 처리해야 한다"
    ↓
research_agent: 정보 수집
    ↓
Supervisor: "이제 writer_agent가 정리해야 한다"
    ↓
writer_agent: 답변 작성
    ↓
Supervisor: "완료"
    ↓
최종 답변
```

### Supervisor 구현
Supervisor는 다음 작업자를 선택하는 LLM 노드다.

```python
def supervisor(state):
    # LLM이 next_agent를 결정 ("research_agent" | "writer_agent" | "FINISH")
    response = llm.invoke(messages_with_worker_list)
    return {"next": response.next}
```

### 서브그래프
각 에이전트는 독립적인 StateGraph로 구현할 수 있다.

## 구현할 그래프

```
START → supervisor ──→ research_agent ─┐
                  └──→ writer_agent   ─┴→ supervisor
                  └──→ FINISH ──→ END
```

## 뼈대 코드 구조

```
backend/
├── graph/
│   ├── __init__.py
│   ├── state.py           ← 공유 상태 (next 필드 추가)
│   ├── supervisor.py      ← supervisor 노드  ← 핵심 추가
│   ├── agents/
│   │   ├── research.py    ← research_agent
│   │   └── writer.py      ← writer_agent
│   └── graph.py           ← 전체 조합
├── main.py
└── requirements.txt
```

## TODO

`state.py`:
- [ ] `next: str` 필드 추가 (supervisor가 다음 에이전트를 지정)
- [ ] `research_result: str` 필드 추가 (에이전트 간 결과 전달)

`supervisor.py`:
- [ ] LLM에게 가능한 작업자 목록("research_agent", "writer_agent", "FINISH")을 제공
- [ ] 응답에서 `next` 값을 파싱하여 반환

`agents/research.py`:
- [ ] 주어진 질문으로 FAQ + 상품 정보를 수집
- [ ] 결과를 `research_result` 상태에 저장

`agents/writer.py`:
- [ ] `research_result`를 바탕으로 최종 답변 작성

`graph.py`:
- [ ] supervisor의 conditional edge: `state["next"]` 값으로 분기

## 체크포인트

```python
# "노트북 구매 시 배송비와 환불 정책을 알려줘"
# 흐름: supervisor → research(상품+FAQ 조회) → supervisor → writer(답변 작성) → FINISH
```
