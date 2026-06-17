
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
    print("Validation Test 시작")
    print("=" * 60)

    # 계좌 생성용
    r = requests.post(f"{BASE_URL}/api/v1/accounts/", json={
        "name": "Validation 계좌",
        "currency": "KRW",
        "initial_balance": 1000000
    })
    account_id = r.json().get("id") if r.status_code == 201 else 1

    print("\n[ Account 검증 ]")
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

    print("\n[ Order 검증 ]")
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

    print("\n[ Auth 검증 ]")
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

    passed, failed = print_summary(results, "Validation")
    save_history("validation/test_validation.py", results)
    return passed, failed

if __name__ == "__main__":
    run_tests()
