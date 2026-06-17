
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
    print("Smoke Test 시작")
    print("=" * 60)

    # Health
    print("\n[ Health ]")
    r = requests.get(f"{BASE_URL}/api/v1/health/")
    check("GET /api/v1/health/ → 200", r.status_code == 200)

    # Auth
    print("\n[ Auth ]")
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
    print("\n[ Accounts ]")
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
    print("\n[ Orders ]")
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
    print("\n[ Positions ]")
    r = requests.get(f"{BASE_URL}/api/v1/positions/")
    check("GET /api/v1/positions/ → 200", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/v1/positions/9999")
    check("GET /api/v1/positions/9999 → 404", r.status_code == 404)

    # Agent Logs
    print("\n[ Agent Logs ]")
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
    print("\n[ Security Events ]")
    r = requests.post(f"{BASE_URL}/api/v1/security-events/", json={
        "event_type": "ATTACK",
        "severity": "HIGH",
        "source": "red-agent",
        "description": "SQL Injection 탐지"
    })
    check("POST /api/v1/security-events/ → 201", r.status_code == 201)

    r = requests.get(f"{BASE_URL}/api/v1/security-events/")
    check("GET /api/v1/security-events/ → 200", r.status_code == 200)

    passed, failed = print_summary(results, "Smoke")
    save_history("smoke/test_api_smoke.py", results)
    return passed, failed

if __name__ == "__main__":
    run_tests()
