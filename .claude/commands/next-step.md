현재 LangGraph 학습 프로젝트의 진행 상황을 파악하고 다음 단계를 스캐폴딩해줘.

## 네가 해야 할 일

### 1단계: 현재 상태 파악

다음을 확인해:
- 루트 디렉토리에 `01-faq-bot/`, `02-tool-use/`, ... 중 어떤 폴더가 있는지
- 가장 최근에 만들어진 폴더(가장 높은 번호)가 어디인지
- 그 폴더의 TODO가 얼마나 완성됐는지 (`graph/nodes.py`, `graph/graph.py` 등에서 `raise NotImplementedError` 또는 `# TODO` 확인)

### 2단계: 완성도 판단

현재 폴더에서:
- `NotImplementedError`가 남아있으면 → **아직 현재 단계를 완성하지 않았음**
  - 어떤 TODO가 남아있는지 알려주고, 완성을 도와주겠냐고 물어봐
- 모두 완성됐으면 → **다음 단계로 넘어갈 준비 완료**

### 3단계: 다음 단계 스캐폴딩

다음 단계로 넘어가기로 했다면:

1. `LEARNING_PATH.md`를 읽어 다음 단계 번호와 이름을 확인
2. `templates/[번호]-[이름]/` 폴더의 파일들을 읽어 뼈대 코드 파악
3. 루트에 `[번호]-[이름]/` 폴더를 생성하고 템플릿 파일들을 복사
   - `graph/` 폴더 전체 복사
   - `main.py` 복사
   - `requirements.txt` 복사
   - `.env.example` 복사 (있으면)
4. 새 폴더에 `frontend/`가 없으면 이전 단계의 `frontend/`를 그대로 복사해도 된다고 알려줘

### 4단계: 학습 안내

스캐폴딩 완료 후:
1. 해당 단계의 `templates/[번호]-[이름]/TEMPLATE.md` 내용 요약
2. **제일 먼저 구현해야 할 파일**과 **TODO 순서** 안내
3. "막히면 언제든지 물어보세요!" 멘트로 마무리

## 참고사항

- 단계 매핑:
  - 01: basic-graph (완성 기준: 01-faq-bot)
  - 02: tool-use
  - 03: react-agent
  - 04: multi-agent
  - 05: human-in-loop
  - 06: memory
  - 07: streaming
  - 08: production
- 한국어로 대화할 것
- 파일을 복사할 때는 Write 도구를 사용하고, 내용은 Read로 먼저 읽어올 것
- 08까지 모두 완성했다면 축하 메시지와 함께 "다음엔 실제 서비스에 붙여볼까요?" 제안
