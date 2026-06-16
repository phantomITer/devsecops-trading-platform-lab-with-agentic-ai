# tests/e2e/test_e2e.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from tests.utils.base import check, save_history, print_summary

BASE_URL = "http://127.0.0.1:8000"


def run_tests():
    results = []

    print("\n" + "=" * 60)
    print("E2E Test 시작")
    print("=" * 60 + "\n")

    # ──────────────────────────────────────────────
    # 전체 거래 흐름: 계좌생성 → 종목조회 → 주문생성 → 주문조회
    # ──────────────────────────────────────────────
    print("[ 전체 거래 흐름 ]")

    # 1) 계좌 생성
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "E2E Test Account",
        "currency": "USD",
        "initial_balance": 100000
    })
    check(results, "1) 계좌 생성 → 201", r.status_code == 201)
    account_id = r.json().get("id") if r.status_code == 201 else None

    # 2) 계좌 단건 조회
    r = requests.get(f"{BASE_URL}/api/accounts/{account_id}")
    check(results, "2) 계좌 단건 조회 → 200", r.status_code == 200)
    check(results, "2) 계좌 잔고 확인 (100000)",
          r.json().get("initial_balance") == 100000)

    # 3) 종목 목록 조회
    r = requests.get(f"{BASE_URL}/api/instruments?market=US&type=STOCK")
    check(results, "3) 미국 주식 종목 조회 → 200", r.status_code == 200)
    check(results, "3) 종목 1개 이상 존재", len(r.json()) > 0)

    # 4) 종목 단건 조회
    r = requests.get(f"{BASE_URL}/api/instruments/AAPL")
    check(results, "4) AAPL 종목 조회 → 200", r.status_code == 200)
    check(results, "4) AAPL symbol 확인",
          r.json().get("symbol") == "AAPL")

    # 5) LIMIT 주문 생성
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": 10,
        "price": 190.5
    })
    check(results, "5) LIMIT 주문 생성 → 201", r.status_code == 201)
    limit_order_id = r.json().get("id") if r.status_code == 201 else None
    check(results, "5) 주문 status = NEW",
          r.json().get("status") == "NEW")

    # 6) MARKET 주문 생성
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "TSLA",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 5
    })
    check(results, "6) MARKET 주문 생성 → 201", r.status_code == 201)
    market_order_id = r.json().get("id") if r.status_code == 201 else None
    check(results, "6) MARKET 주문 price = None",
          r.json().get("price") is None)

    # 7) 주문 목록 조회
    r = requests.get(f"{BASE_URL}/api/orders")
    check(results, "7) 주문 목록 조회 → 200", r.status_code == 200)
    check(results, "7) 주문 2개 이상 존재", len(r.json()) >= 2)

    # 8) LIMIT 주문 단건 조회
    r = requests.get(f"{BASE_URL}/api/orders/{limit_order_id}")
    check(results, "8) LIMIT 주문 단건 조회 → 200", r.status_code == 200)
    check(results, "8) 주문 symbol = AAPL",
          r.json().get("symbol") == "AAPL")
    check(results, "8) 주문 quantity = 10.0",
          r.json().get("quantity") == 10.0)
    check(results, "8) 주문 price = 190.5",
          r.json().get("price") == 190.5)

    # 9) MARKET 주문 단건 조회
    r = requests.get(f"{BASE_URL}/api/orders/{market_order_id}")
    check(results, "9) MARKET 주문 단건 조회 → 200", r.status_code == 200)
    check(results, "9) 주문 symbol = TSLA",
          r.json().get("symbol") == "TSLA")

    passed, failed = print_summary(results, "E2E")
    save_history("e2e/test_e2e.py", results)
    return passed, failed


if __name__ == "__main__":
    run_tests()