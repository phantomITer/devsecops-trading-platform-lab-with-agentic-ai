📁 DevSecOps Trading Platform Lab - 생성/수정 파일 목록 (최신화)

✅ Phase 1 완료 기준 (79/79 테스트 통과)

🗂️ 루트 레벨

text

📄 run.py                          # 메인 실행 엔트리포인트

📄 requirements.txt                # 전체 의존성

📄 .env                            # 환경변수

📄 .gitignore

📄 README.md

📄 setup\_files.py                  # 파일 자동생성 스크립트

📄 fix\_failures.py                 # 테스트 실패 수정 스크립트

🗂️ app/ (FastAPI 백엔드)

text

📄 app/\_\_init\_\_.py

📄 app/main.py                     # FastAPI 앱 진입점, 라우터 등록, redirect\_slashes=False



📁 app/core/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 config.py                   # 환경설정 (Settings 클래스)

&#x20;   📄 database.py                 # SQLAlchemy 엔진/세션

&#x20;   📄 security.py                 # JWT, 패스워드 해싱



📁 app/models/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 user.py                     # User ORM 모델

&#x20;   📄 account.py                  # Account ORM 모델

&#x20;   📄 order.py                    # Order ORM 모델

&#x20;   📄 position.py                 # Position ORM 모델

&#x20;   📄 market\_data.py              # MarketData ORM 모델

&#x20;   📄 agent\_log.py                # AgentLog ORM 모델 (unique agent\_id 처리)

&#x20;   📄 security\_event.py           # SecurityEvent ORM 모델



📁 app/schemas/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 user.py                     # Pydantic User 스키마

&#x20;   📄 account.py                  # Pydantic Account 스키마

&#x20;   📄 order.py                    # Pydantic Order 스키마

&#x20;   📄 position.py                 # Pydantic Position 스키마

&#x20;   📄 market\_data.py              # Pydantic MarketData 스키마

&#x20;   📄 agent\_log.py                # Pydantic AgentLog 스키마

&#x20;   📄 security\_event.py           # Pydantic SecurityEvent 스키마



📁 app/services/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 user\_service.py             # 사용자 CRUD, 인증

&#x20;   📄 accounts\_service.py         # 계좌 생성/조회 (IntegrityError 처리)

&#x20;   📄 orders\_service.py           # 주문 처리 로직

&#x20;   📄 positions\_service.py        # 포지션 관리

&#x20;   📄 market\_data\_service.py      # pykrx 연동, 시세 조회

&#x20;   📄 agent\_log\_service.py        # 에이전트 로그 기록

&#x20;   📄 security\_event\_service.py   # 보안 이벤트 기록/조회



📁 app/api/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📁 app/api/v1/

&#x20;       📄 \_\_init\_\_.py

&#x20;       📄 router.py               # v1 통합 라우터

&#x20;       📄 auth.py                 # /auth/login, /auth/register

&#x20;       📄 users.py                # /users/ CRUD

&#x20;       📄 accounts.py             # /accounts/ (prefix 중복 수정)

&#x20;       📄 orders.py               # /orders/ CRUD

&#x20;       📄 positions.py            # /positions/ 조회

&#x20;       📄 market\_data.py          # /market-data/ KRX 시세

&#x20;       📄 agent\_logs.py           # /agent-logs/

&#x20;       📄 security\_events.py      # /security-events/



📁 app/middleware/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 logging\_middleware.py       # 요청 로깅

&#x20;   📄 security\_middleware.py      # 보안 헤더



📁 app/utils/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 helpers.py                  # 공통 유틸



🗂️ tests/ (Phase 1 완료)

text

📁 tests/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 conftest.py                 # pytest fixtures

&#x20;   📄 test\_smoke.py               # 스모크 테스트

&#x20;   📄 test\_integration.py         # 통합 테스트 (unique agent\_id 처리)

&#x20;   📄 test\_validation.py          # 데이터 유효성 검사 테스트

&#x20;   📄 test\_security.py            # 보안 테스트 (SQL Injection, Auth)

&#x20;   📄 test\_e2e.py                 # End-to-End 시나리오 테스트

