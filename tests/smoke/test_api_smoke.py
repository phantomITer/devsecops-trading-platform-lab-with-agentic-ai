# tests/smoke/test_api_smoke.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from tests.utils.base import check, save_history, print_summary

BASE_URL = "http://127.0.0.1:8000"


def run_tests():
    results = []

    print("\n" + "=" * 60)
    print("Smoke Test 시작")
    print("=" * 60 + "\n")

    # ──────────────────────────────────────────────
    # 1. Health
    # ──────────────────────────────────────────────
    print("[ Health ]")
    r = requests.get(f"{BASE_URL}/api/health")
    check(results, "GET /api/health → 200", r.status_code == 200, str(r.json()))

    # ──────────────────────────────────────────────
    # 2. Accounts
    # ──────────────────────────────────────────────
    print("\n[ Accounts ]")

    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "Test Account",
        "currency": "USD",
        "initial_balance": 10000
    })
    check(results, "POST /api/accounts → 201", r.status_code == 201, str(r.json()))
    account_id = r.json().get("id") if r.status_code == 201 else None

    r = requests.get(f"{BASE_URL}/api/accounts")
    check(results, "GET /api/accounts → 200", r.status_code == 200, f"{len(r.json())}개")

    if account_id:
        r = requests.get(f"{BASE_URL}/api/accounts/{account_id}")
        check(results, f"GET /api/accounts/{account_id} → 200", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/accounts/9999")
    check(results, "GET /api/accounts/9999 → 404", r.status_code == 404)

    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "Bad Account",
        "currency": "USD",
        "initial_balance": -1
    })
    check(results, "POST /api/accounts (initial_balance=-1) → 4xx", r.status_code in (400, 422))

    # ──────────────────────────────────────────────
    # 3. Orders
    # ──────────────────────────────────────────────
    print("\n[ Orders ]")

    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": 10,
        "price": 190.5
    })
    check(results, "POST /api/orders → 201", r.status_code == 201, str(r.json()))
    order_id = r.json().get("id") if r.status_code == 201 else None

    r = requests.get(f"{BASE_URL}/api/orders")
    check(results, "GET /api/orders → 200", r.status_code == 200, f"{len(r.json())}개")

    if order_id:
        r = requests.get(f"{BASE_URL}/api/orders/{order_id}")
        check(results, f"GET /api/orders/{order_id} → 200", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/orders/9999")
    check(results, "GET /api/orders/9999 → 404", r.status_code == 404)

    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": -1,
        "price": 190.5
    })
    check(results, "POST /api/orders (quantity=-1) → 4xx", r.status_code in (400, 422))

    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": 10
    })
    check(results, "POST /api/orders (LIMIT, price 없음) → 4xx", r.status_code in (400, 422))

    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": 9999,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 10
    })
    check(results, "POST /api/orders (account_id=9999) → 400", r.status_code == 400)

    # ──────────────────────────────────────────────
    # 4. Instruments
    # ──────────────────────────────────────────────
    print("\n[ Instruments ]")

    r = requests.get(f"{BASE_URL}/api/instruments")
    check(results, "GET /api/instruments → 200", r.status_code == 200, f"{len(r.json())}개")

    r = requests.get(f"{BASE_URL}/api/instruments?market=KOSPI")
    check(results, "GET /api/instruments?market=KOSPI → 200", r.status_code == 200, f"{len(r.json())}개")

    r = requests.get(f"{BASE_URL}/api/instruments?q=삼성")
    check(results, "GET /api/instruments?q=삼성 → 200", r.status_code == 200, f"{len(r.json())}개")

    r = requests.get(f"{BASE_URL}/api/instruments/AAPL")
    check(results, "GET /api/instruments/AAPL → 200", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/instruments/aapl")
    check(results, "GET /api/instruments/aapl → 200 (대소문자 무시)", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/instruments/XYZ")
    check(results, "GET /api/instruments/XYZ → 404", r.status_code == 404)

    # ──────────────────────────────────────────────
    # 결과 요약 + 이력 저장
    # ──────────────────────────────────────────────
    passed, failed = print_summary(results, "Smoke")
    save_history("smoke/test_api_smoke.py", results)
    return passed, failed


if __name__ == "__main__":
    run_tests()