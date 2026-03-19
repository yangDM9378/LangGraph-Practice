from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from graph.tools import tools

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024)

SYSTEM_PROMPT = """당신은 고객 지원 에이전트입니다.
복잡한 질문에는 여러 도구를 단계적으로 사용해 답하세요.
한국어로 답변하세요.

사용 가능한 도구:
- search_faq: 정책/규정 검색
- calculate: 가격 계산
- get_product_info: 상품 정보 조회
"""

# ── 방법 1: create_react_agent 프리빌트 사용 (빠른 구현) ────────────────
# TODO: create_react_agent로 에이전트를 만들어보세요
# graph = create_react_agent(llm, tools=tools, state_modifier=SYSTEM_PROMPT)


# ── 방법 2: StateGraph 직접 구현 (더 많은 제어) ───────────────────────
# TODO: 02-tool-use의 graph.py를 참고해 직접 구현해보세요
# 구조는 동일하지만, System prompt를 더 상세하게 작성하는 것이 핵심


# 두 방법을 번갈아 사용해보며 차이를 비교해보세요
raise NotImplementedError("graph.py를 구현해 주세요 (방법 1 또는 2)")
