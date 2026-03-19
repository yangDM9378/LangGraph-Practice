# 08 · Production — 에러 핸들링, LangSmith 모니터링

## 학습 목표

- [ ] LangSmith로 그래프 실행을 트레이싱하고 시각화
- [ ] 노드 레벨 에러 핸들링과 fallback 패턴 구현
- [ ] 구조화 로깅(JSON 로그)으로 관찰 가능성 확보
- [ ] API Rate Limit 대응 (Retry with exponential backoff)
- [ ] 타임아웃과 입력 검증으로 안정성 향상

## 핵심 개념

### LangSmith 트레이싱
환경 변수만 설정하면 모든 LangChain/LangGraph 호출이 자동으로 트레이싱된다.

```bash
# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=faq-bot-production
```

LangSmith에서 확인 가능:
- 각 노드의 입출력
- LLM 토큰 사용량 및 비용
- 실행 시간 및 병목
- 에러 스택 트레이스

### Fallback 노드 패턴
노드 실행 중 예외가 발생해도 그래프가 중단되지 않게 한다.

```python
def safe_node(state):
    try:
        return risky_operation(state)
    except Exception as e:
        logger.error(f"node failed: {e}", extra={"state": state})
        return {"answer": "죄송합니다. 일시적인 오류가 발생했습니다.", "error": str(e)}
```

### 구조화 로깅

```python
import structlog
logger = structlog.get_logger()

logger.info("node_executed",
    node="classify_question",
    category=category,
    latency_ms=elapsed,
    token_count=response.usage_metadata["total_tokens"]
)
```

### Rate Limit 대응

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_llm_with_retry(messages):
    return llm.invoke(messages)
```

## 체크리스트 (프로덕션 준비)

- [ ] 모든 LLM 호출에 try/except 래핑
- [ ] 에러 발생 시 사용자에게 친화적인 메시지 반환
- [ ] 로그에 node명, latency, token count 포함
- [ ] LangSmith 프로젝트 이름 환경변수로 관리
- [ ] API 키 노출 방지 (환경변수 검증)
- [ ] 입력 길이 제한 (DoS 방지)
- [ ] 응답 시간 제한 (timeout)

## 뼈대 코드 구조

```
backend/
├── graph/
│   ├── __init__.py
│   ├── state.py      ← error 필드 추가
│   ├── nodes.py      ← try/except + 구조화 로깅
│   └── graph.py      ← fallback 엣지
├── middleware/
│   └── logging.py    ← 요청/응답 로깅 미들웨어
├── main.py           ← 전역 에러 핸들러, 입력 검증
├── .env.example      ← LANGCHAIN_* 변수 포함
└── requirements.txt  ← structlog, tenacity 추가
```

## TODO

`.env`:
- [ ] `LANGCHAIN_TRACING_V2=true` 추가
- [ ] `LANGCHAIN_API_KEY` 추가
- [ ] `LANGCHAIN_PROJECT=my-faq-bot` 추가

`nodes.py`:
- [ ] 각 LLM 호출을 try/except로 감싸기
- [ ] `structlog`로 노드 실행 로그 남기기
- [ ] `tenacity` retry 데코레이터 추가

`main.py`:
- [ ] `@app.exception_handler(Exception)` 전역 에러 핸들러
- [ ] 입력 메시지 최대 길이 검증 (예: 1000자)
- [ ] 요청별 고유 ID (correlation_id) 생성

## LangSmith 확인 방법

1. https://smith.langchain.com 접속
2. 프로젝트 "my-faq-bot" 선택
3. 실행 목록에서 트레이스 클릭
4. 각 노드의 입출력, 토큰, 비용 확인
