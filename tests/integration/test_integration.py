
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from tests.utils.base import check as _chk, save_history, print_summary

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    results = []

    def check(name, condition, detail=""):
        _chk(results, name, condition, detail)

    print("\n" + "=" * 60)
    print("Integration Test 시작")
    print("=" * 60)

    # 1. 회원가입 → 로그인
    print("\n[ 회원가입 → 로그인 흐름 ]")
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
    print("\n[ 계좌 생성 → 조회 흐름 ]")
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
    print("\n[ 계좌 → 주문 연동 흐름 ]")
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
    print("\n[ 예외 흐름 ]")
    r = requests.post(f"{BASE_URL}/api/v1/orders/", json={
        "account_id": 9999,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 5
    })
    check("없는 계좌로 주문 → 400", r.status_code == 400)

    # 5. Agent Log → Security Event 연동
    print("\n[ Agent Log → Security Event 연동 ]")
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

    passed, failed = print_summary(results, "Integration")
    save_history("integration/test_integration.py", results)
    return passed, failed

if __name__ == "__main__":
    run_tests()
