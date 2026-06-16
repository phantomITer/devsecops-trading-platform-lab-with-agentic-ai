🚀 구현 절차

현재 상태 재확인

text

✅ 완료: 디렉터리 구조

✅ 완료: app/api/ (health, accounts, orders, instruments)

✅ 완료: app/schemas/

✅ 완료: app/services/

✅ 완료: tests/ (smoke, integration, validation, security, e2e)

✅ 완료: data/instruments.json



❌ 미구현: 나머지 전체





📋 전체 구현 절차

Phase 1 — 백엔드 기반 완성 (app/)

text

Step 1-1. app/core/config.py

&#x20;         환경변수 로드 (.env)

&#x20;         → TRADING\_SERVER\_URL, DB\_URL, SECRET\_KEY



Step 1-2. app/core/security.py

&#x20;         API Key 인증 / JWT 토큰

&#x20;         → 에이전트 인증 기반



Step 1-3. app/core/dependencies.py

&#x20;         FastAPI Depends 정의

&#x20;         → 라우터에서 인증 주입



Step 1-4. app/database.py

&#x20;         SQLAlchemy 연결

&#x20;         → SQLite (개발) → PostgreSQL (운영)



Step 1-5. app/models/

&#x20;         accounts.py / orders.py / instruments.py

&#x20;         → ORM 모델 정의



Step 1-6. app/services/ 확장

&#x20;         기존 서비스에 DB 연동

&#x20;         → accountsservice, ordersservice



Step 1-7. app/adapters/krx\_fetcher.py

&#x20;         pykrx로 국내주식 데이터 수집



Step 1-8. app/adapters/mock\_generator.py

&#x20;         개발용 Mock 시세 생성



Step 1-9. app/api/websocket.py

&#x20;         실시간 시세 브로드캐스트

&#x20;         → WebSocket 엔드포인트



Step 1-10. app/api/health.py 확장

&#x20;          AI heartbeat 흡수

&#x20;          → GET /health/agents

Phase 2 — AI 공통 허브 (agenticAi/core/)

text

Step 2-1. agenticAi/core/base.py

&#x20;         공통 베이스 클래스

&#x20;         → TRADING\_SERVER\_URL

&#x20;         → AGENT\_API\_KEY

&#x20;         → OLLAMA\_URL

&#x20;         → heartbeat 루프



Step 2-2. agenticAi/core/llm/ollama\_client.py

&#x20;         Ollama API 호출 클라이언트

&#x20;         → 모델 선택, 프롬프트 전송, 응답 파싱



Step 2-3. agenticAi/core/llm/prompts.py

&#x20;         AI별 프롬프트 템플릿

&#x20;         → Red용 / Blue용 / 투자자용



Step 2-4. agenticAi/core/tools/market\_data.py

&#x20;         GET /instruments 호출

&#x20;         → 시세 데이터 조회



Step 2-5. agenticAi/core/tools/order.py

&#x20;         POST /orders 호출

&#x20;         → 롱/숏 주문 실행



Step 2-6. agenticAi/core/tools/portfolio.py

&#x20;         GET /accounts 호출

&#x20;         → 계좌/포지션 조회



Step 2-7. agenticAi/core/tools/alert.py

&#x20;         이벤트 알림 전송

&#x20;         → 대시보드로 이벤트 푸시



Step 2-8. agenticAi/core/setup.py

&#x20;         pip install -e . 패키징

Phase 3 — AI 에이전트 구현 (agenticAi/)

text

Step 3-1. agenticAi/blue/ (가장 먼저 — 방어자 선행)

&#x20;         │

&#x20;         ├── kisaRag/loader.py

&#x20;         │   KISA 문서 로드 (PDF/텍스트)

&#x20;         │

&#x20;         ├── kisaRag/vector\_store.py

&#x20;         │   ChromaDB 벡터 저장

&#x20;         │

&#x20;         ├── kisaRag/retriever.py

&#x20;         │   관련 점검항목 검색

&#x20;         │

&#x20;         ├── scanner/web.py

&#x20;         ├── scanner/api.py

&#x20;         ├── scanner/auth.py

&#x20;         ├── scanner/config.py

&#x20;         │   KISA 기준 취약점 점검

&#x20;         │

&#x20;         ├── detector.py

&#x20;         │   실시간 이상탐지

&#x20;         │

&#x20;         ├── analyzer.py

&#x20;         │   LLM 기반 위협 판단

&#x20;         │

&#x20;         ├── reporter.py

&#x20;         │   점검 보고서 생성

&#x20;         │

&#x20;         └── blue.py

&#x20;             Blue AI 오케스트레이터



Step 3-2. agenticAi/red/

&#x20;         │

&#x20;         ├── owasp/a01\~a10

&#x20;         │   OWASP 10개 공격 모듈

&#x20;         │

&#x20;         ├── planner.py

&#x20;         │   Ollama로 공격 전략 수립

&#x20;         │

&#x20;         ├── logger.py

&#x20;         │   공격 이력 기록

&#x20;         │

&#x20;         └── red.py

&#x20;             Red AI 오케스트레이터



Step 3-3. agenticAi/institutional/

&#x20;         institutional.py

&#x20;         → 시장 데이터 수신

&#x20;         → Ollama 판단 (롱/숏/홀드)

&#x20;         → 주문 실행

&#x20;         → 포지션 관리



Step 3-4. agenticAi/retailA/

&#x20;         retail\_a.py

&#x20;         → institutional과 동일 구조

&#x20;         → 개인투자자 특성 프롬프트 적용



Step 3-5. agenticAi/retailB/

&#x20;         retail\_b.py

&#x20;         → retailA와 동일 구조

&#x20;         → 다른 투자 성향 프롬프트

Phase 4 — 프론트엔드

text

Step 4-1. appFrontEnd/

&#x20;         증권 UI

&#x20;         │

&#x20;         ├── 캔들스틱 차트 (lightweight-charts)

&#x20;         ├── 호가창 (OrderBook)

&#x20;         ├── 롱/숏 주문 패널

&#x20;         ├── 포지션/손익 현황

&#x20;         └── WebSocket 실시간 시세 연동



Step 4-2. dashboard/

&#x20;         통합 운영 관제

&#x20;         │

&#x20;         ├── AI 에이전트 상태 (5개)

&#x20;         ├── CPU/메모리/디스크/GPU 모니터링

&#x20;         ├── 네트워크 연결/지연/트래픽

&#x20;         ├── OWASP 히트맵 (Red 공격 현황)

&#x20;         └── KISA 점검 현황 (Blue 방어 현황)

Phase 5 — 인프라

text

Step 5-1. infra/Dockerfile

&#x20;         FastAPI 컨테이너 이미지



Step 5-2. infra/docker-compose.yml

&#x20;         전체 서비스 오케스트레이션

&#x20;         → app + db + dashboard



Step 5-3. infra/cloud/githubActions/red\_runner.yml

&#x20;         Red AI 무료 클라우드 실행

&#x20;         GitHub Actions 워크플로우

전체 구현 흐름 요약

text

Phase 1          Phase 2          Phase 3

────────         ────────         ────────

app/core/    →   agenticAi/   →   agenticAi/

app/models/      core/            blue/

app/database     (공통 허브)      red/

app/adapters/                     institutional/

app/api/ws                        retailA/

&#x20;                                 retailB/

&#x20;    │                │                │

&#x20;    └────────────────┴────────────────┘

&#x20;                      │

&#x20;             Phase 4 (프론트엔드)

&#x20;             appFrontEnd/ + dashboard/

&#x20;                      │

&#x20;             Phase 5 (인프라)

&#x20;             Docker + GitHub Actions

지금 바로 시작 — Phase 1 순서

text

1-1 → 1-2 → 1-3   (core/ 설정/인증/의존성)

&#x20;     ↓

1-4 → 1-5          (database + models)

&#x20;     ↓

1-6                 (services DB 연동)

&#x20;     ↓

1-7 → 1-8          (adapters 데이터 수집)

&#x20;     ↓

1-9 → 1-10         (WebSocket + health 확장)



