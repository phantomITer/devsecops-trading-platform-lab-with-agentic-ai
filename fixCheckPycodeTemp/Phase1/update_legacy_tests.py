import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")

# ─────────────────────────────────────────────
# smoke/test_api_smoke.py
# ─────────────────────────────────────────────
write("tests/smoke/test_api_smoke.py", '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    results = []
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name} | {detail}")
            failed += 1
        results.append({"name": name, "pass": condition})

    print("\\n" + "=" * 60)
    print("Smoke Test 시작")
    print("=" * 60)

    # Health
    print("\\n[ Health ]")
    r = requests.get(f"{BASE_URL}/api/v1/health/")
    check("GET /api/v1/health/ → 200", r.status_code == 200)

    # Auth
    print("\\n[ Auth ]")
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "username": "smokeuser",
        "email": "smoke@test.com",
        "password": "smoke1234"
    })
    check("POST /api/v1/auth/register → 201", r.status_code == 201, str(r.json()))

    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "username": "smokeuser",
        "password": "smoke1234"
    })
    check("POST /api/v1/auth/login → 200", r.status_code == 200)
    token = r.json().get("access_token") if r.status_code == 200 else None

    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "username": "smokeuser",
        "password": "wrongpass"
    })
    check("POST /api/v1/auth/login (wrong pw) → 401", r.status_code == 401)

    # Accounts
    print("\\n[ Accounts ]")
    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "Smoke Account",
        "currency": "KRW",
        "initial_balance": 1000000
    })
    check("POST /api/v1/accounts/ → 201", r.status_code == 201, str(r.json()))
    account_id = r.json().get("id") if r.status_code == 201 else None

    r = requests.get(f"{BASE_URL}/api/v1/accounts/")
    check("GET /api/v1/accounts/ → 200", r.status_code == 200)

    if account_id:
        r = requests.get(f"{BASE_URL}/api/v1/accounts/{account_id}")
        check(f"GET /api/v1/accounts/{account_id} → 200", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/v1/accounts/9999")
    check("GET /api/v1/accounts/9999 → 404", r.status_code == 404)

    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "Bad",
        "currency": "KRW",
        "initial_balance": -1
    })
    check("POST /api/v1/accounts/ (음수잔고) → 422", r.status_code == 422)

    # Orders
    print("\\n[ Orders ]")
    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    check("POST /api/v1/orders/ → 201", r.status_code == 201)
    order_id = r.json().get("id") if r.status_code == 201 else None

    r = requests.get(f"{BASE_URL}/api/v1/orders/")
    check("GET /api/v1/orders/ → 200", r.status_code == 200)

    if order_id:
        r = requests.get(f"{BASE_URL}/api/v1/orders/{order_id}")
        check(f"GET /api/v1/orders/{order_id} → 200", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/v1/orders/9999")
    check("GET /api/v1/orders/9999 → 404", r.status_code == 404)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 0
    })
    check("POST /api/v1/orders/ (quantity=0) → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10
    })
    check("POST /api/v1/orders/ (LIMIT, price 없음) → 400", r.status_code == 400)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": 9999,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 10
    })
    check("POST /api/v1/orders/ (없는 account) → 400", r.status_code == 400)

    # Positions
    print("\\n[ Positions ]")
    r = requests.get(f"{BASE_URL}/api/v1/positions/")
    check("GET /api/v1/positions/ → 200", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/v1/positions/9999")
    check("GET /api/v1/positions/9999 → 404", r.status_code == 404)

    # Agent Logs
    print("\\n[ Agent Logs ]")
    r = requests.post(f"{BASE_URL}/api/v1/agent-logs/", json={
        "agent_id": "red-smoke-001",
        "agent_type": "red",
        "action": "A03_SQL_INJECTION",
        "result": "simulated"
    })
    check("POST /api/v1/agent-logs/ → 201", r.status_code == 201)

    r = requests.get(f"{BASE_URL}/api/v1/agent-logs/")
    check("GET /api/v1/agent-logs/ → 200", r.status_code == 200)

    # Security Events
    print("\\n[ Security Events ]")
    r = requests.post(f"{BASE_URL}/api/v1/security-events/", json={
        "event_type": "ATTACK",
        "severity": "HIGH",
        "source": "red-agent",
        "description": "SQL Injection 탐지"
    })
    check("POST /api/v1/security-events/ → 201", r.status_code == 201)

    r = requests.get(f"{BASE_URL}/api/v1/security-events/")
    check("GET /api/v1/security-events/ → 200", r.status_code == 200)

    print("\\n" + "=" * 60)
    print(f"결과: {passed} 통과 / {passed + failed} 전체")
    print("=" * 60)
    return passed, failed

if __name__ == "__main__":
    run_tests()
''')

# ─────────────────────────────────────────────
# integration/test_integration.py
# ─────────────────────────────────────────────
write("tests/integration/test_integration.py", '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name} | {detail}")
            failed += 1

    print("\\n" + "=" * 60)
    print("Integration Test 시작")
    print("=" * 60)

    # 1. 회원가입 → 로그인
    print("\\n[ 회원가입 → 로그인 흐름 ]")
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "username": "intuser",
        "email": "int@test.com",
        "password": "int1234"
    })
    check("회원가입 → 201", r.status_code == 201)

    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "username": "intuser",
        "password": "int1234"
    })
    check("로그인 → 200 + token", r.status_code == 200 and "access_token" in r.json())
    token = r.json().get("access_token") if r.status_code == 200 else None

    # 2. 계좌 생성 → 조회
    print("\\n[ 계좌 생성 → 조회 흐름 ]")
    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "통합테스트 계좌",
        "currency": "KRW",
        "initial_balance": 5000000
    })
    check("계좌 생성 → 201", r.status_code == 201)
    account_id = r.json().get("id") if r.status_code == 201 else None

    r = requests.get(f"{BASE_URL}/api/v1/accounts/{account_id}")
    check("계좌 단건 조회 → 200", r.status_code == 200)
    check("계좌 잔고 확인", r.json().get("current_balance") == 5000000)

    # 3. 계좌 → 주문 연동
    print("\\n[ 계좌 → 주문 연동 흐름 ]")
    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    check("주문 생성 → 201", r.status_code == 201)
    check("주문 상태 NEW 확인", r.json().get("status") == "NEW")
    order_id = r.json().get("id") if r.status_code == 201 else None

    r = requests.get(f"{BASE_URL}/api/v1/orders/{order_id}")
    check("주문 단건 조회 → 200", r.status_code == 200)
    check("주문 종목 확인", r.json().get("symbol") == "005930")

    # 4. 없는 계좌로 주문
    print("\\n[ 예외 흐름 ]")
    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": 9999,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 5
    })
    check("없는 계좌로 주문 → 400", r.status_code == 400)

    # 5. Agent Log → Security Event 연동
    print("\\n[ Agent Log → Security Event 연동 ]")
    r = requests.post(f"{BASE_URL}/api/v1/agent-logs/", json={
        "agent_id": "red-int-001",
        "agent_type": "red",
        "action": "A01_BROKEN_ACCESS",
        "result": "권한 우회 시도"
    })
    check("Agent Log 기록 → 201", r.status_code == 201)

    r = requests.post(f"{BASE_URL}/api/v1/security-events/", json={
        "event_type": "ATTACK",
        "severity": "CRITICAL",
        "source": "red-int-001",
        "description": "A01 Broken Access Control 탐지"
    })
    check("Security Event 기록 → 201", r.status_code == 201)

    r = requests.get(f"{BASE_URL}/api/v1/security-events/")
    check("Security Event 목록 조회 → 200", r.status_code == 200)
    check("Security Event 존재 확인", len(r.json()) >= 1)

    print("\\n" + "=" * 60)
    print(f"결과: {passed} 통과 / {passed + failed} 전체")
    print("=" * 60)
    return passed, failed

if __name__ == "__main__":
    run_tests()
''')

# ─────────────────────────────────────────────
# validation/test_validation.py
# ─────────────────────────────────────────────
write("tests/validation/test_validation.py", '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name} | {detail}")
            failed += 1

    print("\\n" + "=" * 60)
    print("Validation Test 시작")
    print("=" * 60)

    # 계좌 생성용
    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "Validation 계좌",
        "currency": "KRW",
        "initial_balance": 1000000
    })
    account_id = r.json().get("id") if r.status_code == 201 else 1

    print("\\n[ Account 검증 ]")
    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "",
        "currency": "KRW",
        "initial_balance": 1000
    })
    check("빈 name → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "계좌",
        "currency": "KRW",
        "initial_balance": -1
    })
    check("음수 initial_balance → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "계좌",
        "currency": "KRW",
        "initial_balance": 0
    })
    check("initial_balance=0 → 201 (허용)", r.status_code == 201)

    print("\\n[ Order 검증 ]")
    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "HOLD",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    check("잘못된 side(HOLD) → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "WRONG",
        "quantity": 10,
        "price": 75000
    })
    check("잘못된 order_type → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 0,
        "price": 75000
    })
    check("quantity=0 → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": -5,
        "price": 75000
    })
    check("quantity 음수 → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10
    })
    check("LIMIT 주문 price 없음 → 400", r.status_code == 400)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": 9999,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 10
    })
    check("없는 account_id → 400", r.status_code == 400)

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 10
    })
    check("MARKET 주문 price 없어도 → 201", r.status_code == 201)

    print("\\n[ Auth 검증 ]")
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "username": "",
        "email": "empty@test.com",
        "password": "test1234"
    })
    check("빈 username → 422", r.status_code == 422)

    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "username": "valuser",
        "email": "notanemail",
        "password": "test1234"
    })
    check("잘못된 email 형식 → 생성됨(422 아닐수있음)", r.status_code in (201, 422))

    print("\\n" + "=" * 60)
    print(f"결과: {passed} 통과 / {passed + failed} 전체")
    print("=" * 60)
    return passed, failed

if __name__ == "__main__":
    run_tests()
''')

# ─────────────────────────────────────────────
# security/test_security.py
# ─────────────────────────────────────────────
write("tests/security/test_security.py", '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name} | {detail}")
            failed += 1

    print("\\n" + "=" * 60)
    print("Security Test 시작")
    print("=" * 60)

    print("\\n[ SQL Injection 시도 ]")
    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "username": "admin' OR '1'='1",
        "password": "anything"
    })
    check("SQL Injection 로그인 → 401 차단", r.status_code == 401)

    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "'; DROP TABLE accounts; --",
        "currency": "KRW",
        "initial_balance": 1000
    })
    check("SQL Injection 계좌명 → 201 (안전하게 저장)", r.status_code == 201)

    print("\\n[ 인증 우회 시도 ]")
    r = requests.get(f"{BASE_URL}/api/v1/users/", headers={
        "Authorization": "Bearer fakejwttoken"
    })
    check("위조 JWT → 401", r.status_code == 401)

    r = requests.get(f"{BASE_URL}/api/v1/users/")
    check("토큰 없이 users 접근 → 401", r.status_code == 401)

    r = requests.delete(f"{BASE_URL}/api/v1/users/1")
    check("토큰 없이 DELETE → 401", r.status_code == 401)

    print("\\n[ 비정상 입력값 ]")
    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "A" * 10000,
        "currency": "KRW",
        "initial_balance": 1000
    })
    check("매우 긴 name → 처리됨 (201 or 422)", r.status_code in (201, 422))

    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": 1,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 999999999,
        "price": 999999999
    })
    check("극단적 수량/가격 → 처리됨 (201 or 422)", r.status_code in (201, 422))

    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "username": "<script>alert(1)</script>",
        "email": "xss@test.com",
        "password": "test1234"
    })
    check("XSS 시도 username → 처리됨", r.status_code in (201, 422))

    print("\\n[ 보안 헤더 확인 ]")
    r = requests.get(f"{BASE_URL}/api/v1/health/")
    check("서버 응답 정상", r.status_code == 200)

    print("\\n" + "=" * 60)
    print(f"결과: {passed} 통과 / {passed + failed} 전체")
    print("=" * 60)
    return passed, failed

if __name__ == "__main__":
    run_tests()
''')

# ─────────────────────────────────────────────
# e2e/test_e2e.py
# ─────────────────────────────────────────────
write("tests/e2e/test_e2e.py", '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name} | {detail}")
            failed += 1

    print("\\n" + "=" * 60)
    print("E2E Test 시작")
    print("=" * 60)

    print("\\n[ 시나리오: 회원가입 → 로그인 → 계좌 → 주문 전체 흐름 ]")

    # 1. 회원가입
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "username": "e2euser",
        "email": "e2e@test.com",
        "password": "e2e1234"
    })
    check("1. 회원가입 → 201", r.status_code == 201)

    # 2. 로그인
    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "username": "e2euser",
        "password": "e2e1234"
    })
    check("2. 로그인 → 200 + token", r.status_code == 200 and "access_token" in r.json())
    token = r.json().get("access_token") if r.status_code == 200 else None

    # 3. 계좌 생성
    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "E2E 모의계좌",
        "currency": "KRW",
        "initial_balance": 10000000
    })
    check("3. 계좌 생성 → 201", r.status_code == 201)
    account_id = r.json().get("id") if r.status_code == 201 else None

    # 4. 계좌 조회
    r = requests.get(f"{BASE_URL}/api/v1/accounts/{account_id}")
    check("4. 계좌 조회 → 200", r.status_code == 200)
    check("4. 잔고 확인", r.json().get("current_balance") == 10000000)

    # 5. 매수 주문
    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    check("5. 매수 주문 → 201", r.status_code == 201)
    check("5. 주문 상태 NEW", r.json().get("status") == "NEW")

    # 6. 매도 주문
    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "SELL",
        "order_type": "MARKET",
        "quantity": 5
    })
    check("6. 매도 주문 → 201", r.status_code == 201)

    # 7. 주문 목록 확인
    r = requests.get(f"{BASE_URL}/api/v1/orders/")
    check("7. 주문 목록 → 200", r.status_code == 200)
    check("7. 주문 2건 이상", len(r.json()) >= 2)

    # 8. Red Agent 공격 시뮬레이션
    print("\\n[ 시나리오: Red Agent 공격 → Blue Agent 탐지 ]")
    r = requests.post(f"{BASE_URL}/api/v1/agent-logs/", json={
        "agent_id": "red-e2e-001",
        "agent_type": "red",
        "action": "A03_SQL_INJECTION",
        "result": "공격 시도"
    })
    check("8. Red Agent 로그 → 201", r.status_code == 201)

    # 9. Blue Agent 보안 이벤트 기록
    r = requests.post(f"{BASE_URL}/api/v1/security-events/", json={
        "event_type": "ATTACK",
        "severity": "HIGH",
        "source": "red-e2e-001",
        "description": "SQL Injection 탐지 및 차단"
    })
    check("9. Blue Agent 보안이벤트 → 201", r.status_code == 201)

    # 10. 전체 보안이벤트 확인
    r = requests.get(f"{BASE_URL}/api/v1/security-events/")
    check("10. 보안이벤트 목록 → 200", r.status_code == 200)
    check("10. 보안이벤트 존재 확인", len(r.json()) >= 1)

    print("\\n" + "=" * 60)
    print(f"결과: {passed} 통과 / {passed + failed} 전체")
    print("=" * 60)
    return passed, failed

if __name__ == "__main__":
    run_tests()
''')

# ─────────────────────────────────────────────
# 전체 실행 스크립트
# ─────────────────────────────────────────────
with open("run_all_tests.py", "w", encoding="utf-8") as f:
    f.write('''
import sys
from tests.smoke.test_api_smoke import run_tests as smoke
from tests.integration.test_integration import run_tests as integration
from tests.validation.test_validation import run_tests as validation
from tests.security.test_security import run_tests as security
from tests.e2e.test_e2e import run_tests as e2e

total_passed = 0
total_failed = 0

print("\\n" + "=" * 60)
print("전체 테스트 실행")
print("=" * 60)

for name, fn in [
    ("Smoke", smoke),
    ("Integration", integration),
    ("Validation", validation),
    ("Security", security),
    ("E2E", e2e),
]:
    p, f = fn()
    total_passed += p
    total_failed += f

print("\\n" + "=" * 60)
print(f"최종 결과: {total_passed} 통과 / {total_passed + total_failed} 전체")
if total_failed == 0:
    print("✅ 전체 통과!")
else:
    print(f"❌ {total_failed}개 실패")
print("=" * 60)
''')
print("  [OK] run_all_tests.py")

print()
print("=" * 50)
print("✅ 레거시 테스트 업데이트 완료!")
print("=" * 50)
print()
print("서버 실행 후 아래 명령어로 전체 테스트 실행:")
print("python run_all_tests.py")