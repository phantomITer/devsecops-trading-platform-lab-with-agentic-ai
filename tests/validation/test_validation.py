# tests/validation/test_validation.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
import time
from tests.utils.base import check, save_history, print_summary

BASE_URL = "http://127.0.0.1:8000"


def run_tests():
    results = []

    print("\n" + "=" * 60)
    print("Validation Test 시작")
    print("=" * 60 + "\n")

    # 선행: 계좌 생성
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": f"Validation-{int(time.time())}",
        "currency": "USD",
        "initial_balance": 10000
    })
    account_id = r.json().get("id") if r.status_code == 201 else None

    # ──────────────────────────────────────────────
    # Accounts 검증
    # ──────────────────────────────────────────────
    print("[ Accounts 검증 ]")

    # initial_balance 음수
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "Bad", "currency": "USD", "initial_balance": -1
    })
    check(results, "initial_balance=-1 → 4xx", r.status_code in (400, 422))

    # initial_balance 0 (경계값, 허용)
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": f"Zero-{int(time.time())}", "currency": "USD", "initial_balance": 0
    })
    check(results, "initial_balance=0 → 201 (허용)", r.status_code == 201)

    # name 빈 문자열
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "", "currency": "USD", "initial_balance": 1000
    })
    check(results, "name='' → 4xx", r.status_code in (400, 422))

    # 필수 필드 누락 (name 없음)
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "currency": "USD", "initial_balance": 1000
    })
    check(results, "name 누락 → 422", r.status_code == 422)

    # 필수 필드 누락 (currency 없음)
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "No Currency", "initial_balance": 1000
    })
    check(results, "currency 누락 → 422", r.status_code == 422)

    # ──────────────────────────────────────────────
    # Orders 검증
    # ──────────────────────────────────────────────
    print("\n[ Orders 검증 ]")

    # quantity 0
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "BUY", "type": "LIMIT", "quantity": 0, "price": 190.5
    })
    check(results, "quantity=0 → 4xx", r.status_code in (400, 422))

    # quantity 음수
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "BUY", "type": "LIMIT", "quantity": -1, "price": 190.5
    })
    check(results, "quantity=-1 → 4xx", r.status_code in (400, 422))

    # LIMIT 주문 price 없음
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "BUY", "type": "LIMIT", "quantity": 10
    })
    check(results, "LIMIT price 없음 → 4xx", r.status_code in (400, 422))

    # LIMIT 주문 price=0
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "BUY", "type": "LIMIT", "quantity": 10, "price": 0
    })
    check(results, "LIMIT price=0 → 4xx", r.status_code in (400, 422))

    # LIMIT 주문 price 음수
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "BUY", "type": "LIMIT", "quantity": 10, "price": -1
    })
    check(results, "LIMIT price=-1 → 4xx", r.status_code in (400, 422))

    # MARKET 주문 price 있어도 허용
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "BUY", "type": "MARKET", "quantity": 10, "price": 190.5
    })
    check(results, "MARKET price 있어도 → 201 (허용)", r.status_code == 201)

    # 존재하지 않는 account_id
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": 9999, "symbol": "AAPL",
        "side": "BUY", "type": "MARKET", "quantity": 10
    })
    check(results, "account_id=9999 → 400", r.status_code == 400)

    # 잘못된 side 값
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "INVALID", "type": "MARKET", "quantity": 10
    })
    check(results, "side=INVALID → 4xx", r.status_code in (400, 422))

    # 잘못된 type 값
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id, "symbol": "AAPL",
        "side": "BUY", "type": "INVALID", "quantity": 10
    })
    check(results, "type=INVALID → 4xx", r.status_code in (400, 422))

    passed, failed = print_summary(results, "Validation")
    save_history("validation/test_validation.py", results)
    return passed, failed


if __name__ == "__main__":
    run_tests()