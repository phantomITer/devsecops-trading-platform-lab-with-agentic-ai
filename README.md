# DevSecOps Trading Platform Lab with Agentic AI

본 프로젝트는 진보하는 AI기반 사이버공격에 따라 경각심을 가지며 안전하고 신뢰성있는 "모의 트레이딩(증권거래 시스템) 플랫폼"를 구현해보면서 DevSecOps with Agentic AI 거버넌스를 조성하기 위한 경험을 수행해보고자 추진하는 개인 프로젝트입니다.

> ※ 본 프로젝트는 교육 및 역량강화 목적입니다. 따라서 본 프로젝트을 통하여 범죄 영감 획득, 악성 행위 활용 등의 경우에는 국내외 법에 따른 저촉을 받을 수 있으며, 본인에게는 책임이 없음을 명시합니다. 프로젝트 성공/실패 여하와 관계없이 결과물 구현에 노력하겠습니다.
> 
>  
> 

---

## 📋 진행 현황 (Progress)

| Phase | 내용 | 상태 |
|-------|------|------|
| **Phase 1** | 백엔드 API / DB / 테스트 체계 | ✅ **완료** (71/71 테스트 통과) |
| **Phase 2** | Agentic AI Core 라이브러리 | 🔜 진행 예정 |
| **Phase 3** | 5개 에이전트 구현 (Red/Blue/기관/개인A/개인B) | ⏳ 대기 |
| **Phase 4** | Frontend (투자자용) + Dashboard (운영자용) | ⏳ 대기 |
| **Phase 5** | Infra / Cloud / CI/CD 배포 | ⏳ 대기 |

## 🛠️ Technology Stack

| 기술 | 용도 |
|------|------|
| Python 3.10+ | 백엔드 및 에이전트 주 언어 |
| FastAPI | 트레이딩 백엔드 REST API 프레임워크 |
| Uvicorn | FastAPI ASGI 서버 |
| Pydantic v2 | 요청/응답 스키마 및 데이터 검증 |
| SQLAlchemy + SQLite | 로컬 개발용 ORM + DB |
| MySQL / PostgreSQL | 운영 환경 데이터베이스 (예정) |
| pykrx | KRX 국내 주식 실시간 시세 |
| python-jose + passlib | JWT 인증 및 패스워드 해싱 |
| Ollama | 로컬 LLM 실행 (llama3, mistral 등) |
| ChromaDB / FAISS | 벡터 DB (RAG 엔진용) |
| React / Vue | 프론트엔드 SPA (예정) |
| Docker / Docker Compose | 컨테이너화 (예정) |
| GitHub Actions | CI/CD 파이프라인 (예정) |
| SAST/DAST 도구 | 보안 스캔 자동화 (예정) |
| Azure (Arc/하이브리드) | 클라우드 연동 (예정) |

---

## ⚡ Quick Start

### 1. 사전 요구사항
- Python 3.10 이상
- Git
- Windows / Linux 환경

### 2. 저장소 클론

```bash
git clone https://github.com/phantomITer/devsecops-trading-platform-lab-with-agentic-ai.git
cd devsecops-trading-platform-lab-with-agentic-ai
```

### 3. 가상환경 설정

```bash
python -m venv .venv

# Windows (cmd)
.\.venv\Scripts\Activate

# macOS / Linux
source .venv/bin/activate
```

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

### 5. 서버 실행

```bash
# 방법 1: run.py 사용 (권장)
python run.py

# 방법 2: uvicorn 직접 실행
uvicorn app.main:app --reload
```

### 6. 동작 확인

| 항목 | URL |
|------|-----|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost/redoc` |
| 헬스 체크 | `http://localhost:8000/api/v1/health` |

### 7. 테스트 실행

```bash
pytest tests/ -v
```

---

## 🌐 API 전체 목록

### Auth

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| POST | `/api/v1/auth/register` | 회원가입 | 201 |
| POST | `/api/v1/auth/login` | 로그인 (JWT 발급) | 200 |

### Users

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| GET | `/api/v1/users/` | 사용자 목록 조회 | 200 |
| GET | `/api/v1/users/{id}` | 사용자 단건 조회 | 200 / 404 |
| PUT | `/api/v1/users/{id}` | 사용자 수정 | 200 / 404 |
| DELETE | `/api/v1/users/{id}` | 사용자 삭제 | 204 / 404 |

### Accounts

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| GET | `/api/v1/accounts/` | 계좌 목록 조회 | 200 |
| POST | `/api/v1/accounts/` | 계좌 생성 | 201 |
| GET | `/api/v1/accounts/{id}` | 계좌 단건 조회 | 200 / 404 |

### Orders

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| GET | `/api/v1/orders/` | 주문 목록 조회 | 200 |
| POST | `/api/v1/orders/` | 주문 생성 | 201 |
| GET | `/api/v1/orders/{id}` | 주문 단건 조회 | 200 / 404 |

### Positions

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| GET | `/api/v1/positions/` | 포지션 목록 조회 | 200 |
| GET | `/api/v1/positions/{id}` | 포지션 단건 조회 | 200 / 404 |

### Market Data

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| GET | `/api/v1/market-data/` | 시세 목록 조회 | 200 |
| GET | `/api/v1/market-data/{symbol}` | 종목 시세 조회 (pykrx) | 200 / 404 |

### Agent Logs

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| GET | `/api/v1/agent-logs/` | 에이전트 로그 목록 | 200 |
| POST | `/api/v1/agent-logs/` | 에이전트 로그 기록 | 201 |

### Security Events

| 메서드 | URL | 기능 | 상태 코드 |
|--------|-----|------|-----------|
| GET | `/api/v1/security-events/` | 보안 이벤트 목록 | 200 |
| POST | `/api/v1/security-events/` | 보안 이벤트 기록 | 201 |

---

## 📐 Domain & Validation Rules

### Accounts

`POST /api/v1/accounts/`

| 필드 | 타입 | 규칙 |
|------|------|------|
| `name` | string | 필수, 빈 문자열 불가 |
| `currency` | string | 필수 (예: `"KRW"`, `"USD"`) |
| `initial_balance` | float | 필수, `>= 0` (음수 불가) |

### Orders

`POST /api/v1/orders/`

| 필드 | 타입 | 규칙 |
|------|------|------|
| `account_id` | int | 필수, 존재하는 계좌 ID여야 함 |
| `symbol` | string | 필수 (예: `"005930"` 삼성전자) |
| `side` | string | `"BUY"` 또는 `"SELL"` 만 허용 |
| `order_type` | string | `"MARKET"` 또는 `"LIMIT"` 만 허용 |
| `quantity` | float | 필수, `> 0` |
| `price` | float | LIMIT 주문 시 필수 `> 0` / MARKET 주문 시 무시 |

### 에러 응답 예시

| 상황 | 상태 코드 | 메시지 |
|------|-----------|--------|
| `initial_balance` 음수 | 422 | `"Input should be greater than or equal to 0"` |
| `quantity` 0 이하 | 400 | `"Quantity must be greater than 0"` |
| LIMIT 주문 price 없음 | 400 | `"Limit orders require a positive price"` |
| 존재하지 않는 `account_id` | 400 | `"Account {id} does not exist"` |
| 잘못된 `side` / `type` 값 | 422 | `"Input should be 'BUY' or 'SELL'"` |
| 중복 `agent_id` | 409 | `"Agent ID already exists"` |

---

---

## ✨ Features

### ✅ 현재 구현된 기능 (Phase 1 완료)

#### 🔧 FastAPI 백엔드 API
- **인증/인가**: JWT 기반 로그인 / 회원가입 (`/api/v1/auth/`)
- **사용자 관리**: User CRUD (`/api/v1/users/`)
- **계좌 관리**: Account 생성/조회 (`/api/v1/accounts/`)
- **주문 처리**: Order 생성/조회, 도메인 검증 (`/api/v1/orders/`)
- **포지션 관리**: Position 조회 (`/api/v1/positions/`)
- **시장 데이터**: KRX 실시간 시세 (pykrx 연동) (`/api/v1/market-data/`)
- **에이전트 로그**: Agent 실행 로그 기록/조회 (`/api/v1/agent-logs/`)
- **보안 이벤트**: 보안 이벤트 기록/조회 (`/api/v1/security-events/`)
- **Swagger UI** 자동 문서화 (`/docs`)

#### 🗄️ 데이터베이스
- SQLAlchemy ORM + SQLite (로컬 개발)
- 7개 ORM 모델: User, Account, Order, Position, MarketData, AgentLog, SecurityEvent
- 도메인 검증 규칙: 수량/가격/계좌 존재 여부 등

#### 🧪 테스트 체계 (79/79 통과)
- **Smoke**: 전체 API 기본 동작 확인
- **Validation**: 데이터 유효성 검사
- **Integration**: 계좌→주문 연동 흐름
- **Security**: SQL Injection, 인증 우회 등 보안 시나리오
- **E2E**: 전체 거래 흐름 (회원가입→로그인→계좌→주문)

---


## 🤖 Agentic AI 구성 (Phase 2~3 예정)

### 에이전트 역할

| 에이전트 | 역할 | 프레임워크 |
|----------|------|-----------|
| 🔴 **Red Agent** | OWASP Top 10 기반 웹 취약점 공격 시뮬레이션 | Ollama LLM + 공격 모듈 |
| 🔵 **Blue Agent** | KISA 기술적 취약점 분석 가이드 기반 RAG 방어 | Ollama LLM + RAG (KISA PDF) |
| 🏦 **Institutional Agent** | 기관투자자 전략 (TWAP/VWAP, MPT, VaR) | Ollama LLM + pykrx |
| 👤 **Retail Agent A** | 개인투자자 A - 공격적 단타 (모멘텀, RSI/MACD) | Ollama LLM + pykrx |
| 👤 **Retail Agent B** | 개인투자자 B - 보수적 장기 (가치투자, 배당) | Ollama LLM + pykrx |

### Red Agent - OWASP Top 10 공격 시나리오

| # | 취약점 | 시뮬레이션 대상 |
|---|--------|----------------|
| A01 | Broken Access Control | 계좌/주문 권한 우회 시도 |
| A02 | Cryptographic Failures | 암호화 미적용 데이터 탈취 시도 |
| A03 | Injection | SQL Injection, Command Injection |
| A04 | Insecure Design | 비즈니스 로직 우회 |
| A05 | Security Misconfiguration | 설정 오류 탐지 및 악용 |
| A06 | Vulnerable Components | 취약한 라이브러리 탐지 |
| A07 | Auth & Session Failures | JWT 위변조, 세션 탈취 |
| A08 | Software Integrity Failures | 무결성 검증 우회 |
| A09 | Logging & Monitoring Failures | 로그 우회, 탐지 회피 |
| A10 | SSRF | 내부 서버 요청 위조 |

### Blue Agent - KISA RAG 방어 흐름

> KISA 주요정보통신기반시설 기술적 취약점 분석 가이드
> → PDF 청킹 & 임베딩
> → ChromaDB / FAISS 벡터스토어
> → 쿼리 (Red Agent 공격 이벤트)
> → 관련 대응 가이드라인 검색 & 생성
> → 보안 이벤트 기록 (`/api/v1/security-events/`)
> → 대응 조치 실행 + 알림 발송

---

## 🧪 Tests

### 테스트 현황 (Phase 1 기준)

| 파일 | 테스트 수 | 상태 | 설명 |
|------|-----------|------|------|
| `test_api_smoke.py` | 19개 | ✅ 통과 | 전체 API 기본 동작 확인 |
| `test_validation.py` | 18개 | ✅ 통과 | 데이터 유효성 검증 |
| `test_integration.py` | 17개 | ✅ 통과 | 계좌→주문 연동 흐름 |
| `test_security.py` | 14개 | ✅ 통과 | SQL Injection, 인증 우회 등 |
| `test_e2e.py` | 11개 | ✅ 통과 | 전체 거래 흐름 E2E |
| **합계** | **79개** | ✅ **79/79** | |

### 실행 방법

전체 테스트 실행

```bash
python run_all_tests.py
pytest tests/ -v  
```

카테고리별 실행

```bash
python  tests/smoke/test_api_smoke.py -v
python  tests/validation/test_validation.py -v
python  tests/integration/test_integration.py -v
python  tests/e2e/test_e2e.py -v
```

## 🗺️ Roadmap

### ✅ 완료 (Phase 1)

- FastAPI 백엔드 전체 구조 구축
- SQLAlchemy ORM + SQLite DB 연동
- 7개 도메인 모델 (User, Account, Order, Position, MarketData, AgentLog, SecurityEvent)
- JWT 인증/인가
- pykrx KRX 시장 데이터 연동
- 도메인 검증 규칙 전체 적용
- 테스트 체계 구축 및 79/79 통과
- 보안 미들웨어 (헤더, 로깅)

### 🔜 진행 예정 (Phase 2)

- `agenticAi/core/` 공통 라이브러리 구현
  - `base.py` - 베이스 에이전트 클래스
  - `llm/ollama_client.py` - Ollama LLM 클라이언트
  - `llm/rag_engine.py` - KISA 문서 기반 RAG 엔진
  - `tools/` - 공통 툴 레지스트리
  - `memory_store.py` - 에이전트 메모리/상태 관리

### 📋 대기 중 (Phase 3)

- 🔴 Red Agent: OWASP Top 10 공격 시뮬레이션 (10개 공격 모듈)
- 🔵 Blue Agent: KISA RAG 기반 탐지 및 방어
- 🏦 Institutional Agent: 기관투자자 자동매매 (MPT/TWAP/VWAP)
- 👤 Retail Agent A: 단타 투자자 자동매매 (모멘텀/기술적 분석)
- 👤 Retail Agent B: 장기 투자자 자동매매 (가치투자/배당)

### 📋 대기 중 (Phase 4)

- 투자자용 프론트엔드 (`appfrontend/`) - OO증권 UI 스타일
- 운영자 대시보드 (`dashboard/`) - Azure 포털 스타일
  - 에이전트 실시간 모니터링
  - 보안 이벤트 시각화

### 📋 대기 중 (Phase 5)

- Docker / Docker Compose 컨테이너화
- GitHub Actions CI/CD 파이프라인
- SAST / DAST / 이미지 스캔 자동화
- Azure Arc 하이브리드 클라우드 연동

---

## 🔒 Security Architecture

### 보안 레이어 구성

| 레이어 | 구성 요소 | 상태 |
|--------|-----------|------|
| **API 보안** | JWT 인증, 보안 헤더 미들웨어 | ✅ Phase 1 완료 |
| **입력 검증** | Pydantic v2 스키마 검증 | ✅ Phase 1 완료 |
| **공격 시뮬레이션** | Red Agent OWASP Top 10 | ⏳ Phase 3 예정 |
| **방어 자동화** | Blue Agent KISA RAG | ⏳ Phase 3 예정 |
| **정적 분석** | SAST (Bandit, Semgrep) | ⏳ Phase 5 예정 |
| **동적 분석** | DAST (OWASP ZAP) | ⏳ Phase 5 예정 |
| **컨테이너 보안** | 이미지 스캔 (Trivy) | ⏳ Phase 5 예정 |
| **클라우드 보안** | Azure Defender, Arc | ⏳ Phase 5 예정 |

---

## 📊 Database Schema

### 주요 테이블

| 테이블 | 주요 컬럼 | 설명 |
|--------|-----------|------|
| `users` | id, username, email, hashed_password | 사용자 |
| `accounts` | id, user_id, name, currency, balance | 모의 계좌 |
| `orders` | id, account_id, symbol, side, order_type, quantity, price, status |
| `positions` | id, account_id, symbol, quantity, avg_price | 보유 포지션 |
| `market_data` | id, symbol, price, volume, timestamp | KRX 시세 |
| `agent_logs` | id, agent_id, agent_type, action, result, timestamp | 에이전트 로그 |
| `security_events` | id, event_type, severity, source, description, timestamp | 보안 이벤트 |

---

## 📝 개발 규칙 (Conventions)

### 네이밍 규칙

| 대상 | 규칙 | 예시 |
|------|------|------|
| 디렉터리/폴더 | camelCase | `agenticAi/`, `redAgent/` |
| Python 파일 | snake_case | `base_agent.py`, `red_agent.py` |
| Python 클래스 | PascalCase | `BaseAgent`, `RedAgent` |
| Python 함수/변수 | snake_case | `get_account()`, `agent_id` |
| JS 컴포넌트 | camelCase | `securityPanel.js`, `agentMonitor.js` |
| API 엔드포인트 | kebab-case | `/security-events/`, `/market-data/` |
| DB 테이블/컬럼 | snake_case | `agent_logs`, `created_at` |

### 에이전트 독립 실행 원칙

각 에이전트는 독립 패키지로 실행 가능합니다.

```bash
# 에이전트 독립 실행 (Phase 3 이후)
python agenticAi/redAgent/run.py
python agenticAi/blueAgent/run.py
python agenticAi/institutionalAgent/run.py
python agenticAi/retailAgentA/run.py
python agenticAi/retailAgentB/run.py

# 전체 에이전트 통합 실행
python agenticAi/run.py
```

### 코드 스타일

- Python: PEP8 준수, Black 포매터
- 최대 줄 길이: 88자
- 타입 힌트 필수 (`def func(x: int) -> str:`)
- Docstring: Google 스타일

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

- **목적**: 정보보안 전문가 역량강화 (DevSecOps + AI Agent + 금융 시스템)
- **기술 스택**: Python, FastAPI, SQLAlchemy, Ollama, pykrx, Docker, Azure
- **참고 문서**:
  - [OWASP Top 10](https://owasp.org/www-project-top-ten/)
  - [KISA 주요정보통신기반시설 기술적 취약점 분석 가이드](https://www.kisa.or.kr)
  - [FastAPI 공식 문서](https://fastapi.tiangolo.com)
  - [pykrx 공식 문서](https://github.com/sharebook-kr/pykrx)
