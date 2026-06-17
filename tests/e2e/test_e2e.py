
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
    print("E2E Test 시작")
    print("=" * 60)

    print("\n[ 시나리오: 회원가입 → 로그인 → 계좌 → 주문 전체 흐름 ]")

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
    print("\n[ 시나리오: Red Agent 공격 → Blue Agent 탐지 ]")
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

    passed, failed = print_summary(results, "E2E")
    save_history("e2e/test_e2e.py", results)
    return passed, failed

if __name__ == "__main__":
    run_tests()
