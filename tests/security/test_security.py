# tests/security/test_security.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from tests.utils.base import check, save_history, print_summary

BASE_URL = "http://127.0.0.1:8000"


def run_tests():
    results = []

    print("\n" + "=" * 60)
    print("Security Test 시작")
    print("=" * 60 + "\n")

    # 선행: 계좌 생성
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "Security Test Account",
        "currency": "USD",
        "initial_balance": 10000
    })
    account_id = r.json().get("id") if r.status_code == 201 else None

    # ──────────────────────────────────────────────
    # 1. 입력값 조작 시도
    # ──────────────────────────────────────────────
    print("[ 입력값 조작 시도 ]")

    # SQL Injection (symbol 필드)
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "' OR 1=1 --",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 10
    })
    check(results, "SQL Injection (symbol) → 서버 500 아님",
          r.status_code != 500)

    # XSS 시도 (name 필드)
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "<script>alert('xss')</script>",
        "currency": "USD",
        "initial_balance": 1000
    })
    check(results, "XSS 시도 (name) → 서버 500 아님",
          r.status_code != 500)

    # ──────────────────────────────────────────────
    # 2. 비정상 값 시도
    # ──────────────────────────────────────────────
    print("\n[ 비정상 값 시도 ]")

    # 매우 큰 quantity
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 999999999999
    })
    check(results, "quantity=999999999999 → 서버 500 아님",
          r.status_code != 500)

    # 매우 큰 price
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": 1,
        "price": 999999999999
    })
    check(results, "price=999999999999 → 서버 500 아님",
          r.status_code != 500)

    # 매우 큰 initial_balance
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "Big Balance",
        "currency": "USD",
        "initial_balance": 999999999999
    })
    check(results, "initial_balance=999999999999 → 서버 500 아님",
          r.status_code != 500)

    # ──────────────────────────────────────────────
    # 3. 잘못된 JSON 형식
    # ──────────────────────────────────────────────
    print("\n[ 잘못된 요청 형식 ]")

    # 빈 body
    r = requests.post(f"{BASE_URL}/api/accounts",
                      data="",
                      headers={"Content-Type": "application/json"})
    check(results, "빈 body → 4xx",
          r.status_code in (400, 422))

    # 완전히 잘못된 JSON
    r = requests.post(f"{BASE_URL}/api/accounts",
                      data="NOT JSON",
                      headers={"Content-Type": "application/json"})
    check(results, "잘못된 JSON → 4xx",
          r.status_code in (400, 422))

    # ──────────────────────────────────────────────
    # 4. 존재하지 않는 엔드포인트
    # ──────────────────────────────────────────────
    print("\n[ 존재하지 않는 엔드포인트 ]")

    r = requests.get(f"{BASE_URL}/api/nonexistent")
    check(results, "GET /api/nonexistent → 404",
          r.status_code == 404)

    r = requests.delete(f"{BASE_URL}/api/accounts/1")
    check(results, "DELETE /api/accounts/1 → 405 (미구현)",
          r.status_code in (404, 405))

    # ──────────────────────────────────────────────
    # 5. 타입 오류 시도
    # ──────────────────────────────────────────────
    print("\n[ 타입 오류 시도 ]")

    # account_id 에 문자열
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": "abc",
        "symbol": "AAPL",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 10
    })
    check(results, "account_id=abc → 422",
          r.status_code == 422)

    # quantity 에 문자열
    r = requests.post(f"{BASE_URL}/api/orders", json={
        "account_id": account_id,
        "symbol": "AAPL",
        "side": "BUY",
        "type": "MARKET",
        "quantity": "abc"
    })
    check(results, "quantity=abc → 422",
          r.status_code == 422)

    # initial_balance 에 문자열
    r = requests.post(f"{BASE_URL}/api/accounts", json={
        "name": "Type Error",
        "currency": "USD",
        "initial_balance": "abc"
    })
    check(results, "initial_balance=abc → 422",
          r.status_code == 422)

    passed, failed = print_summary(results, "Security")
    save_history("security/test_security.py", results)
    return passed, failed


if __name__ == "__main__":
    run_tests()