# 02 · Tool Use — @tool, ToolNode, bind_tools

## 학습 목표

- [ ] `@tool` 데코레이터로 LangChain 도구 정의
- [ ] `llm.bind_tools(tools)`로 LLM에 도구 연결
- [ ] `ToolNode`가 tool_call을 자동 실행하는 원리 이해
- [ ] `tools_condition`으로 도구 호출 여부에 따라 분기
- [ ] `MessagesState`의 메시지 누적 흐름 파악

## 핵심 개념

### @tool
LangChain 도구 정의. docstring이 LLM에게 도구 설명으로 전달된다.

```python
@tool
def search_faq(query: str) -> str:
    """FAQ 데이터베이스에서 관련 항목을 검색합니다."""
    # 실제 검색 로직
    return "검색 결과"
```

### bind_tools
LLM이 도구를 사용할 수 있도록 바인딩. LLM은 필요시 tool_call을 응답에 포함시킨다.

```python
llm_with_tools = llm.bind_tools([search_faq, get_order_status])
```

### ToolNode
메시지에서 tool_call을 꺼내 실행하고 결과를 ToolMessage로 반환하는 특수 노드.

```python
from langgraph.prebuilt import ToolNode
tool_node = ToolNode([search_faq, get_order_status])
```

### tools_condition
마지막 AI 메시지에 tool_call이 있으면 `"tools"`, 없으면 `"end"` 반환.

```python
from langgraph.prebuilt import tools_condition
builder.add_conditional_edges("agent", tools_condition)
```

## 구현할 그래프

```
START → agent ──(tool_call 있음)──→ tools ──→ agent
              └──(tool_call 없음)──→ END
```

## 뼈대 코드 구조

```
backend/
├── graph/
│   ├── __init__.py
│   ├── state.py      ← MessagesState 확장
│   ├── tools.py      ← @tool 함수들  ← 핵심 추가 파일
│   ├── nodes.py      ← agent 노드 (bind_tools 사용)
│   └── graph.py      ← ToolNode 통합
├── main.py
└── requirements.txt
```

## TODO

`tools.py`:
- [ ] `search_faq(query: str) -> str` 구현 (FAQ 딕셔너리 검색)
- [ ] `get_order_status(order_id: str) -> str` 구현 (주문 상태 조회)

`nodes.py`:
- [ ] `llm.bind_tools(tools)` 적용
- [ ] `agent` 노드: messages 기반으로 LLM 호출

`graph.py`:
- [ ] `ToolNode` 등록
- [ ] `tools_condition` conditional edge 추가

## 체크포인트

```python
# 도구가 올바르게 바인딩됐는지 확인
result = llm_with_tools.invoke("주문 12345의 배송 상태를 알려주세요")
print(result.tool_calls)  # tool_call이 포함돼야 함
```
