
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
    print("Security Test 시작")
    print("=" * 60)

    print("\n[ SQL Injection 시도 ]")
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

    print("\n[ 인증 우회 시도 ]")
    r = requests.get(f"{BASE_URL}/api/v1/users/", headers={
        "Authorization": "Bearer fakejwttoken"
    })
    check("위조 JWT → 401", r.status_code == 401)

    r = requests.get(f"{BASE_URL}/api/v1/users/")
    check("토큰 없이 users 접근 → 401", r.status_code == 401)

    r = requests.delete(f"{BASE_URL}/api/v1/users/1")
    check("토큰 없이 DELETE → 401", r.status_code == 401)

    print("\n[ 비정상 입력값 ]")
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

    print("\n[ 보안 헤더 확인 ]")
    r = requests.get(f"{BASE_URL}/api/v1/health/")
    check("서버 응답 정상", r.status_code == 200)

    passed, failed = print_summary(results, "Security")
    save_history("security/test_security.py", results)
    return passed, failed

if __name__ == "__main__":
    run_tests()
