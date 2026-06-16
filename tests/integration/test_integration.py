# tests/integration/test_integration.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from tests.utils.base import check, save_history, print_summary

BASE_URL = "http://127.0.0.1:8000"


def run_tests():
    results = []

    print("\n" + "=" * 60)
    print("Integration Test 시작")
    print("=" * 60 + "\n")

    # ──────────────────────────────────────────────
    # 계좌 → 주문 연동 흐름
    # ──────────────────────────────────────────────
    print("[ 계좌 → 주문 연동 흐름 ]")

    # 1) 계좌 생성
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "Integration Account",
        "currency": "USD",
        "initial_balance": 50000
    })
    check(results, "계좌 생성 → 201", r.status_code == 201)
    account_id = r.json().get("id") if r.status_code == 201 else None

    # 2) 생성된 계좌가 목록에 있는지
    r = requests.get(f"{BASE_URL}/api/accounts")
    account_ids = [a["id"] for a in r.json()]
    check(results, "생성된 계좌가 목록에 포함", account_id in account_ids)

    # 3) 생성된 계좌 단건 조회
    r = requests.get(f"{BASE_URL}/api/accounts/{account_id}")
    check(results, "생성된 계좌 단건 조회 → 200", r.status_code == 200)
    check(results, "계좌 initial_balance = 50000",
          r.json().get("initial_balance") == 50000)
    check(results, "계좌 current_balance = 50000",
          r.json().get("current_balance") == 50000)

    # 4) 해당 계좌로 주문 생성
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "TSLA",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": 5,
        "price": 250.0
    })
    check(results, "주문 생성 → 201", r.status_code == 201)
    order_id = r.json().get("id") if r.status_code == 201 else None
    check(results, "주문 account_id 일치",
          r.json().get("account_id") == account_id)
    check(results, "주문 status = NEW",
          r.json().get("status") == "NEW")

    # 5) 생성된 주문이 목록에 있는지
    r = requests.get(f"{BASE_URL}/api/orders")
    order_ids = [o["id"] for o in r.json()]
    check(results, "생성된 주문이 목록에 포함", order_id in order_ids)

    # 6) 생성된 주문 단건 조회
    r = requests.get(f"{BASE_URL}/api/orders/{order_id}")
    check(results, "생성된 주문 단건 조회 → 200", r.status_code == 200)
    check(results, "주문 symbol = TSLA",
          r.json().get("symbol") == "TSLA")
    check(results, "주문 quantity = 5.0",
          r.json().get("quantity") == 5.0)
    check(results, "주문 price = 250.0",
          r.json().get("price") == 250.0)

    # ──────────────────────────────────────────────
    # Instruments 연동 흐름
    # ──────────────────────────────────────────────
    print("\n[ Instruments 연동 흐름 ]")

    # 종목 목록에서 symbol 가져와서 주문 생성
    r = requests.get(f"{BASE_URL}/api/instruments?market=US&type=STOCK")
    check(results, "미국 주식 종목 목록 조회 → 200", r.status_code == 200)

    if r.status_code == 200 and len(r.json()) > 0:
        symbol = r.json()[0]["symbol"]

        # 해당 종목으로 주문 생성
        r2 = requests.post(f"{BASE_URL}/api/orders", json={
            "account_id": account_id,
            "symbol": symbol,
            "side": "BUY",
            "type": "MARKET",
            "quantity": 1
        })
        check(results, f"종목({symbol})으로 주문 생성 → 201", r2.status_code == 201)

    passed, failed = print_summary(results, "Integration")
    save_history("integration/test_integration.py", results)
    return passed, failed


if __name__ == "__main__":
    run_tests()