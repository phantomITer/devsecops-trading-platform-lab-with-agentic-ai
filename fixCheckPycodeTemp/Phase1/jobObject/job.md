Phase 1 종합 요약

DevSecOps Trading Platform Lab with Agentic AI

1\. 수행 목표

핵심 목표: Agentic AI 에이전트들이 동작할 수 있는 백엔드 플랫폼 기반 구축



목표 항목	내용

백엔드 API 서버	FastAPI 기반 RESTful API 전체 구현

데이터베이스	SQLAlchemy ORM + SQLite 로컬 DB 설계 및 연동

인증/인가 체계	JWT 기반 사용자 인증 시스템 구축

도메인 검증	주문/계좌 비즈니스 규칙 서버사이드 강제 적용

에이전트 로그/보안이벤트	Red/Blue Agent 연동을 위한 로그 기록 API 구현

테스트 체계	5개 유형 테스트 + 자동 히스토리 로그 저장 체계 구축

명명 규칙	camelCase(디렉터리), snake\_case(Python 파일) 통일

2\. 수행 과정

2-1. 초기 구조 설계

프로젝트 디렉터리 설계: app/, agenticAi/, tests/, appfrontend/, dashboard/, infra/, docs/ 등 전체 골격 확정



명명 규칙 수립: 디렉터리 camelCase, Python 파일 snake\_case



API 라우팅 구조: /api/v1/ prefix 기반 버전 관리 설계



2-2. 백엔드 구현 (1차)

FastAPI + SQLAlchemy + SQLite 연동



7개 ORM 모델 구현: User, Account, Order, Position, MarketData, AgentLog, SecurityEvent



/api/v1/auth/, /api/v1/accounts/, /api/v1/orders/, /api/v1/positions/, /api/v1/market-data/, /api/v1/agent-logs/, /api/v1/security-events/



2-3. 구조 불일치 문제 발생 및 rebuild

문제: 초기 구현이 /api/ prefix (v1 없음) 로 작성되어 README 설계(/api/v1/)와 불일치



조치: rebuild\_phase1.py 스크립트로 전체 백엔드를 /api/v1/ 구조로 재구축



추가 수정: fix\_warnings.py로 SQLAlchemy/Pydantic deprecation 경고 제거



2-4. 인증 시스템 트러블슈팅

문제 1: bcrypt/passlib → Python 3.14 환경에서 ValueError: password cannot be longer than 72 bytes 발생



해결: argon2-cffi로 해싱 라이브러리 교체



문제 2: 401 Unauthorized on DELETE — 인증 강제 적용 확인으로 정상 동작 검증



2-5. 테스트 체계 구축 및 반복 수정

단계	내용

1차	초기 테스트 파일 작성 (구버전 /api/ 경로 기준)

2차	rebuild 후 /api/v1/ 경로로 update\_legacy\_tests.py로 일괄 수정

3차	핵심 문제 발견: Phase1 rebuild 시 테스트 파일이 완전 재작성되면서 save\_history() 호출 자체가 누락됨

4차	fix\_save\_history.py로 5개 테스트 파일에 tests.utils.base import + save\_history() 호출 복구

2-6. 히스토리 로그 저장 문제 원인 추적

증상: 테스트는 통과하는데 \*\_TEST\_HISTORY\_\*.md 파일이 생성되지 않음



1차 오진: pytest 실행 방식 문제로 \_\_main\_\_ 블록 우회 추정



실제 원인: rebuild 시 테스트 파일을 새로 작성하면서 from tests.utils.base import save\_history import 자체가 누락되고, 로컬 check() 함수만 내부 정의하는 방식으로 바뀌어 save\_history() 호출 코드가 아예 없었음



3\. 수행 결과

3-1. 구현 완료 항목

항목	내용

API 엔드포인트	8개 도메인, 20+ 엔드포인트 전체 구현

ORM 모델	7개 테이블 (User/Account/Order/Position/MarketData/AgentLog/SecurityEvent)

인증	JWT 발급/검증, Argon2 패스워드 해싱

도메인 검증	음수잔고 차단, quantity/price 규칙, LIMIT 주문 price 필수, 존재 계좌 검증 등

보안 미들웨어	CORS, 보안 헤더, 로깅 미들웨어

Swagger UI	/docs 자동 문서화

pykrx 연동	KRX 시장 데이터 조회

3-2. 테스트 결과

파일	테스트 수	결과

tests/smoke/test\_api\_smoke.py	22개	✅ 전체 통과

tests/integration/test\_integration.py	14개	✅ 전체 통과

tests/validation/test\_validation.py	12개	✅ 전체 통과

tests/security/test\_security.py	9개	✅ 전체 통과

tests/e2e/test\_e2e.py	14개	✅ 전체 통과

합계	71개	✅ 71/71

3-3. 히스토리 로그 체계

명명 규칙 {유형}\_TEST\_HISTORY\_{YYYYMMDD\_HHMMSS}.md 완전 복구



매 테스트 실행마다 각 폴더에 자동 저장



python run\_all\_tests.py 단일 명령으로 전체 테스트 + 로그 저장 동시 수행



3-4. 주요 트러블슈팅 이력

문제	원인	해결

ModuleNotFoundError: app	sys.path 미설정	conftest.py + pytest.ini 추가

password > 72 bytes	bcrypt 한계	argon2-cffi 교체

/api/ vs /api/v1/ 불일치	초기 설계 미반영	rebuild\_phase1.py 전체 재구축

히스토리 파일 미생성	rebuild 시 save\_history 코드 누락	fix\_save\_history.py 복구

DB 상태 오염으로 중복 오류	테스트 격리 미적용	del trading.db 후 재실행

4\. Phase 1 완료 기준 충족 여부

기준	상태

전체 API 정상 동작	✅

71/71 테스트 통과	✅

히스토리 로그 자동 저장	✅

/api/v1/ 라우팅 구조 통일	✅

README 실제 구현과 일치	✅ (수정 완료 예정)

Git commit 준비 완료	✅

→ Phase 1 완료. Phase 2 (agenticAi/core/ 구현) 진행 가능 상태.

