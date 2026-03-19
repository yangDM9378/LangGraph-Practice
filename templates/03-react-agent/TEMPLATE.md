# 03 · ReAct Agent — 추론-행동 루프

## 학습 목표

- [ ] ReAct(Reason + Act) 패턴의 원리 이해
- [ ] 여러 도구를 조합해 복잡한 질문에 답하는 흐름 구현
- [ ] 에이전트가 스스로 추론 단계를 결정하는 구조 파악
- [ ] `create_react_agent` 프리빌트 vs 직접 구현 비교

## 핵심 개념

### ReAct 패턴
"Reasoning + Acting"의 조합. LLM이 **생각 → 행동 → 관찰**을 반복하며 답에 도달한다.

```
[생각] "배송비를 알려면 FAQ를 찾아봐야겠다"
[행동] search_faq(query="배송비")
[관찰] "기본 배송비는 3,000원입니다"
[생각] "할인 쿠폰이 있는지도 확인해야 한다"
[행동] search_faq(query="배송비 할인")
[관찰] "5만원 이상 구매 시 무료 배송"
[최종 답변] "기본 배송비는 3,000원이며, 5만원 이상 구매 시 무료입니다."
```

### create_react_agent (프리빌트)
LangGraph가 제공하는 완성된 ReAct 에이전트. 빠르게 시작할 때 유용.

```python
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(llm, tools=[search_faq, calculate])
```

### 직접 구현
더 많은 제어가 필요할 때 StateGraph로 직접 구현.

## 구현할 그래프

```
START → agent ──(tool_call)──→ tools ──→ agent ──(tool_call)──→ ...
              └──(완료)──→ END
```

02-tool-use와 구조는 같지만, 도구가 더 많고 추론이 더 복잡하다.

## 추가 도구

```
search_faq(query)        ← 02에서 가져옴
calculate(expression)    ← 새로 추가 (수식 계산)
get_product_info(name)   ← 새로 추가 (상품 정보)
```

## 뼈대 코드 구조

```
backend/
├── graph/
│   ├── __init__.py
│   ├── state.py
│   ├── tools.py      ← 도구 3개
│   ├── nodes.py      ← agent 노드
│   └── graph.py      ← ReAct 그래프
├── main.py
└── requirements.txt
```

## TODO

`tools.py`:
- [ ] `calculate(expression: str) -> str` 구현 (eval 활용, 안전하게)
- [ ] `get_product_info(product_name: str) -> str` 구현

`nodes.py`:
- [ ] System prompt에 "단계적으로 추론하라"는 지시 추가

`graph.py`:
- [ ] `create_react_agent`를 사용해 빠르게 구현해보기
- [ ] 그 다음 StateGraph로 동일하게 직접 구현해보기 (비교)

## 체크포인트

```python
# "3개 상품 각 15,000원 구매 시 총액은? 5만원 이상이면 무료배송인가?"
# → calculate + search_faq를 차례로 호출해야 정답
```
