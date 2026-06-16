\# DevSecOps Trading Platform Lab with Agentic AI



안전하고 신뢰성있는 "모의 트레이딩(증권 시스템) 서비스"를 구현하기 위하여 하이브리드 인프라, DevSecOps for Agentic AI(RedAgent vs BlueAgent)을 수행하는 개인 프로젝트입니다.



\---



\## Features



\### 현재 제공 기능 (1단계 완료)



\- \*\*FastAPI 백엔드 API\*\*

&#x20; - 계좌(Account), 주문(Order), 종목(Instrument) REST API 구현

&#x20; - 도메인 검증 규칙 적용 (수량, 가격, 계좌 존재 여부 등)

&#x20; - Swagger UI 자동 문서화 (`/docs`)



\- \*\*테스트 체계\*\*

&#x20; - smoke / validation / integration / security / e2e 구조로 분리

&#x20; - 테스트 실행 시 결과 이력 자동 저장



\### 계획 중인 기능



\- \*\*DB 연동\*\*: SQLite → MySQL/PostgreSQL (SQLAlchemy)

\- \*\*도메인 확장\*\*: 체결(Trade), 포지션(Position), 잔고(Balance), 감사 로그(AuditLog)

\- \*\*기관-개인 투자자용 프론트엔드\*\*: OO증권과 유사한 UI 스타일 (React/Vue)

\- \*\*운영자 대시보드\*\*: Azure 포털과 유사한 UI 스타일 (카드/타일 기반 하이브리드 대시보드)

\- \*\*DevSecOps 파이프라인\*\*: Docker, GitHub Actions CI/CD, SAST/DAST 등

\- \*\*AI 에이전트 보안 시뮬레이션\*\*: RedAgent(공격 시나리오 자동 생성 및 공격 수행), BlueAgent(취약점 점검, 이상 거래 탐지 및 대응)



\---



\## Technology Stack



\### 현재 사용 중



| 기술 | 용도 |

|------|------|

| Python 3.10+ | 백엔드 애플리케이션 주 언어 |

| FastAPI | 트레이딩 백엔드 REST API 프레임워크 |

| Uvicorn | FastAPI ASGI 서버 |

| Pydantic | 요청/응답 스키마 및 데이터 검증 |



\### 계획된 스택



| 기술 | 용도 |

|------|------|

| SQLAlchemy + SQLite | 로컬 개발용 ORM + DB (진행 중) |

| MySQL / PostgreSQL | 운영 환경 데이터베이스 |

| React / Vue | 프론트엔드 SPA |

| Docker / Docker Compose | 컨테이너화 |

| GitHub Actions | CI/CD 파이프라인 |

| SAST/DAST 도구 | 보안 스캔 자동화 |

| Azure (Arc/하이브리드) | 클라우드 연동 |

| LLM / AI Agent | RedAgent, BlueAgent 보안 시뮬레이션 |

\---



\## Quick Start



\### 1. 사전 요구사항



\- Python 3.10 이상

\- Git

\- Windows, Linux 환경



\### 2. 저장소 클론



```bash

git clone https://github.com/USERNAME/devsecops-trading-platform-lab.git

cd devsecops-trading-platform-lab

```



\### 3. 가상환경 설정



```bash

python -m venv .venv



\# Windows (PowerShell)

.\\.venv\\Scripts\\Activate



\# macOS / Linux

source .venv/bin/activate

```



\### 4. 의존성 설치



```bash

pip install -r requirements.txt

```



\### 5. 서버 실행



```bash

uvicorn app.main:app --reload

```



\### 6. 동작 확인



\- Swagger UI: `http://127.0.0.1:8000/docs`

\- 헬스 체크: `http://127.0.0.1:8000/api/health`



\---



\## Project Structure



```text

devsecops-trading-platform-lab/

&#x20; app/

&#x20;   \_\_init\_\_.py

&#x20;   main.py                  # FastAPI 엔트리포인트

&#x20;   api/                     # 라우터(엔드포인트) 모듈

&#x20;     \_\_init\_\_.py

&#x20;     health.py              # GET /api/health

&#x20;     accounts.py          # GET/POST /api/accounts

&#x20;     orders.py              # GET/POST /api/orders

&#x20;     instruments.py       # GET /api/instruments

&#x20;   schemas/               # Pydantic 요청/응답 스키마

&#x20;     \_\_init\_\_.py

&#x20;     accounts.py

&#x20;     orders.py

&#x20;     instruments.py

&#x20;   services/                # 도메인 비즈니스 로직

&#x20;     \_\_init\_\_.py

&#x20;     accounts\_service.py

&#x20;     orders\_service.py

&#x20; data/

&#x20;   instruments.json      # 예시 종목 데이터 (인메모리 로드)

&#x20; tests/

&#x20;   utils/

&#x20;     \_\_init\_\_.py

&#x20;     base.py               # 공통 유틸 (check, save\_history, print\_summary)

&#x20;   smoke/

&#x20;     test\_api\_smoke.py  # 전체 API 기본 동작 확인

&#x20;   validation/

&#x20;     test\_validation.py   # 검증 규칙 전용

&#x20;   integration/

&#x20;     test\_integration.py  # 계좌→주문 연동 흐름

&#x20;   security/

&#x20;     test\_security.py     # 입력값 조작/보안 시나리오

&#x20;   e2e/

&#x20;     test\_e2e.py          # 전체 거래 흐름

&#x20;   README.md

&#x20; dashboard/             # (계획) Azure 포털 스타일 웹 대시보드

&#x20; infra/                     # (계획) Docker, CI/CD, 보안 스캔

&#x20; requirements.txt

&#x20; README.md

```



\---



\## API 전체 목록



| 메서드 | URL | 기능 | 상태 코드 |

|--------|-----|------|-----------|

| GET | `/api/health` | 서비스 상태 확인 | 200 |

| GET | `/api/accounts/` | 계좌 목록 조회 | 200 |

| POST | `/api/accounts/` | 계좌 생성 | 201 |

| GET | `/api/accounts/{id}` | 계좌 단건 조회 | 200 / 404 |

| GET | `/api/orders/` | 주문 목록 조회 | 200 |

| POST | `/api/orders/` | 주문 생성 | 201 |

| GET | `/api/orders/{id}` | 주문 단건 조회 | 200 / 404 |

| GET | `/api/instruments/` | 종목 목록 조회 (필터/검색) | 200 |

| GET | `/api/instruments/{symbol}` | 종목 단건 조회 | 200 / 404 |



\---



\## Example: Accounts API



\### GET /api/accounts/



모든 계좌 목록을 조회합니다.



\- Method: `GET`

\- URL: `http://localhost:8000/api/accounts/`

\- Response: `200 OK`



예시 응답:



```json

\[

&#x20; {

&#x20;   "id": 1,

&#x20;   "name": "Demo Account 1",

&#x20;   "currency": "USD",

&#x20;   "initial\_balance": 10000.0,

&#x20;   "current\_balance": 10000.0,

&#x20;   "created\_at": "2026-06-16T04:45:00.123456"

&#x20; }

]

```



\### POST /api/accounts/



새 모의 계좌를 생성합니다.



\- Method: `POST`

\- URL: `http://localhost:8000/api/accounts/`

\- Body (JSON):



```json

{

&#x20; "name": "Demo Account 1",

&#x20; "currency": "USD",

&#x20; "initial\_balance": 10000

}

```



\- Response: `201 Created`



예시 응답:



```json

{

&#x20; "id": 1,

&#x20; "name": "Demo Account 1",

&#x20; "currency": "USD",

&#x20; "initial\_balance": 10000.0,

&#x20; "current\_balance": 10000.0,

&#x20; "created\_at": "2026-06-16T04:45:00.123456"

}

```



\### GET /api/accounts/{id}



특정 계좌를 단건 조회합니다.



\- Method: `GET`

\- URL: `http://localhost:8000/api/accounts/{id}`

\- Response: `200 OK` / `404 Not Found`



존재하지 않는 ID 조회 시 `404 Not Found`와 함께 `"Account not found"` 메시지가 반환됩니다.



\---



\## Example: Orders API



\### GET /api/orders/



모든 주문 목록을 조회합니다.



\- Method: `GET`

\- URL: `http://localhost:8000/api/orders/`

\- Response: `200 OK`



예시 응답:



```json

\[

&#x20; {

&#x20;   "id": 1,

&#x20;   "account\_id": 1,

&#x20;   "symbol": "AAPL",

&#x20;   "side": "BUY",

&#x20;   "type": "LIMIT",

&#x20;   "quantity": 10.0,

&#x20;   "price": 190.5,

&#x20;   "status": "NEW",

&#x20;   "created\_at": "2026-06-16T05:00:00.123456"

&#x20; }

]

```



\### POST /api/orders/



새 주문을 생성합니다.



\- Method: `POST`

\- URL: `http://localhost:8000/api/orders/`

\- Body (JSON):



```json

{

&#x20; "account\_id": 1,

&#x20; "symbol": "AAPL",

&#x20; "side": "BUY",

&#x20; "type": "LIMIT",

&#x20; "quantity": 10,

&#x20; "price": 190.5

}

```



\- Response: `201 Created`



\### GET /api/orders/{id}



특정 주문을 단건 조회합니다.



\- Method: `GET`

\- URL: `http://localhost:8000/api/orders/{id}`

\- Response: `200 OK` / `404 Not Found`



존재하지 않는 ID 조회 시 `404 Not Found`와 함께 `"Order not found"` 메시지가 반환됩니다.



\---



\## Example: Instruments API



거래 가능한 종목(주식/ETF) 정보를 조회합니다.  

현재는 `data/instruments.json` 파일에 저장된 예시 데이터를 인메모리로 로드하여 제공합니다.



\### GET /api/instruments/



종목 목록을 조회합니다.



\- Method: `GET`

\- URL: `http://localhost:8000/api/instruments/`

\- Query Params:



| 파라미터 | 필수 | 설명 | 예시 |

|----------|------|------|------|

| `market` | 선택 | 시장 필터 | `KOSPI`, `KOSDAQ`, `US` |

| `type` | 선택 | 종목 유형 필터 | `STOCK`, `ETF` |

| `q` | 선택 | 검색 키워드 (종목명/티커) | `삼성`, `AAPL` |

| `offset` | 선택 | 페이지 시작 인덱스 (default: 0) | `0` |

| `limit` | 선택 | 페이지 크기 (default: 50, max: 200) | `10` |



예시 요청:



```bash

GET /api/instruments?market=US\&type=STOCK

GET /api/instruments?q=삼성

GET /api/instruments?market=KOSPI\&limit=10

```



예시 응답:



```json

\[

&#x20; {

&#x20;   "symbol": "AAPL",

&#x20;   "name": "Apple Inc.",

&#x20;   "market": "US",

&#x20;   "type": "STOCK",

&#x20;   "sector": "Technology",

&#x20;   "currency": "USD",

&#x20;   "current\_price": 190.5,

&#x20;   "change\_percent": -0.5,

&#x20;   "volume": 1000000

&#x20; }

]

```



\### GET /api/instruments/{symbol}



특정 종목을 단건 조회합니다.



```bash

GET http://localhost:8000/api/instruments/AAPL

GET http://localhost:8000/api/instruments/aapl  # 대소문자 구분 없음

```



\- 존재하지 않는 종목: `404 Not Found` + `"Instrument not found"`



\---



\## Domain \& Validation Rules



\### Accounts



`POST /api/accounts/`



| 필드 | 타입 | 규칙 |

|------|------|------|

| `name` | string | 필수, 빈 문자열 불가 |

| `currency` | string | 필수 (예: `"USD"`, `"KRW"`) |

| `initial\_balance` | float | 필수, `>= 0` (음수 불가) |



\### Orders



`POST /api/orders/`



| 필드 | 타입 | 규칙 |

|------|------|------|

| `account\_id` | int | 필수, 존재하는 계좌 ID여야 함 |

| `symbol` | string | 필수 (예: `"AAPL"`) |

| `side` | string | `"BUY"` 또는 `"SELL"` 만 허용 |

| `type` | string | `"MARKET"` 또는 `"LIMIT"` 만 허용 |

| `quantity` | float | 필수, `> 0` (0 이하 불가) |

| `price` | float | LIMIT 주문 시 필수 `> 0` / MARKET 주문 시 무시 |



\### 에러 응답 예시



| 상황 | 상태 코드 | 메시지 |

|------|-----------|--------|

| `initial\_balance` 음수 | 422 | `"Input should be greater than or equal to 0"` |

| `quantity` 0 이하 | 400 | `"Quantity must be greater than 0"` |

| LIMIT 주문 price 없음 | 400 | `"Limit orders require a positive price"` |

| 존재하지 않는 `account\_id` | 400 | `"Account {id} does not exist"` |

| 잘못된 `side` / `type` 값 | 422 | `"Input should be 'BUY' or 'SELL'"` |



\---



\## Tests



테스트는 역할별로 분리된 디렉터리 구조로 관리합니다.  

자세한 내용은 `tests/README.md`를 참고하세요.



\### 실행 방법



```bash

\# 전체 테스트 한번에 실행

python tests/utils/base.py



\# 개별 실행

python tests/smoke/test\_api\_smoke.py

python tests/validation/test\_validation.py

python tests/integration/test\_integration.py

python tests/security/test\_security.py

python tests/e2e/test\_e2e.py

```



\### 현재 테스트 현황



| 파일 | 테스트 수 | 상태 | 설명 |

|------|-----------|------|------|

| `smoke/test\_api\_smoke.py` | 19개 | ✅ 유효 | 전체 API 기본 동작 확인 |

| `validation/test\_validation.py` | - | ⚠️ 일부 유효 | DB 연동 후 완성 예정 |

| `integration/test\_integration.py` | - | ⚠️ 일부 유효 | DB 연동 후 완성 예정 |

| `security/test\_security.py` | - | ⚠️ 일부 유효 | 인증 추가 후 완성 예정 |

| `e2e/test\_e2e.py` | - | ⚠️ 일부 유효 | 도메인 확장 후 완성 예정 |



\---



\## Roadmap



✅ 완료

\- FastAPI 백엔드 스켈레톤

\- Accounts / Orders / Instruments API (GET/POST + 단건 조회)

\- 도메인 검증 규칙 (quantity, price, account\_id 등)

\- 테스트 체계 구축 (smoke/validation/integration/security/e2e)



🔄 진행 중

\- SQLite DB 연동 (SQLAlchemy)



📋 계획

\- MySQL/PostgreSQL 전환

\- 체결(Trade), 포지션(Position), 잔고(Balance) 도메인 추가

\- 감사 로그(AuditLog) 구현

\- 인증/인가 (JWT)

\- 기관-개인 투자자용 프론트엔드 (OO증권 UI 스타일)

\- 운영자 대시보드 (Azure 포털 스타일)

\- Docker/Docker Compose 컨테이너화

\- GitHub Actions CI/CD 파이프라인

\- 보안 스캔 (SAST/DAST/이미지 스캔)

\- RedAgent: 공격 시나리오 자동 생성 및 공격 수행

\- BlueAgent: 취약점 점검, 이상 거래 탐지 및 대응

