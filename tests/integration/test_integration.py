import pytest


class TestIntegration:
    """Integration Test - API 무드 간 연동 흐름 테스트"""

    def test_register_and_login_flow(self, client):
        """회원가입 → 로그인 연동 흐름"""
        # 회원가입
        r = client.post("/api/v1/auth/register", json={
            "username": "intuser",
            "email": "int@test.com",
            "password": "int1234"
        })
        assert r.status_code == 201

        # 로그인
        r = client.post("/api/v1/auth/login", json={
            "username": "intuser",
            "password": "int1234"
        })
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_account_create_and_retrieve(self, client):
        """계좌 생성 → 조회 연동 흐름"""
        # 계좌 생성
        r = client.post("/api/v1/accounts/", json={
            "name": "통합테스트 계좌",
            "currency": "KRW",
            "initial_balance": 5000000
        })
        assert r.status_code == 201
        account_id = r.json()["id"]

        # 단건 조회
        r = client.get(f"/api/v1/accounts/{account_id}")
        assert r.status_code == 200
        assert r.json()["current_balance"] == 5000000

    def test_account_to_order_flow(self, client, test_account):
        """계좌 → 주문 연동 흐름"""
        # 주문 생성
        r = client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "005930",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 10,
            "price": 75000
        })
        assert r.status_code == 201
        assert r.json()["status"] == "NEW"
        order_id = r.json()["id"]

        # 주문 단건 조회
        r = client.get(f"/api/v1/orders/{order_id}")
        assert r.status_code == 200
        assert r.json()["symbol"] == "005930"

    def test_order_invalid_account_returns_400(self, client):
        """없는 계좌로 주문 시 400"""
        r = client.post("/api/v1/orders/", json={
            "account_id": 9999,
            "symbol": "005930",
            "side": "BUY",
            "order_type": "MARKET",
            "quantity": 5
        })
        assert r.status_code == 400

    def test_agent_log_and_security_event_flow(self, client):
        """Agent Log → Security Event 연동 흐름"""
        # Agent Log 기록
        r = client.post("/api/v1/agent-logs/", json={
            "agent_id": "red-int-001",
            "agent_type": "red",
            "action": "A01_BROKEN_ACCESS",
            "result": "권한 우회 시도"
        })
        assert r.status_code == 201

        # Security Event 기록
        r = client.post("/api/v1/security-events/", json={
            "event_type": "ATTACK",
            "severity": "CRITICAL",
            "source": "red-int-001",
            "description": "A01 Broken Access Control 탐지"
        })
        assert r.status_code == 201

        # Security Event 목록 확인
        r = client.get("/api/v1/security-events/")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_full_order_pipeline(self, client, test_account):
        """BUY/SELL 주문 파이프라인 연동"""
        # BUY LIMIT 주문
        r = client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "035420",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 5,
            "price": 100000
        })
        assert r.status_code == 201

        # SELL MARKET 주문
        r = client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "035420",
            "side": "SELL",
            "order_type": "MARKET",
            "quantity": 3
        })
        assert r.status_code == 201

        # 주문 목록 2건 이상
        r = client.get("/api/v1/orders/")
        assert r.status_code == 200
        assert len(r.json()) >= 2

    def test_multiple_accounts_isolation(self, client):
        """복수 계좌 독립성 확인"""
        r1 = client.post("/api/v1/accounts/", json={
            "name": "계좌 A",
            "currency": "KRW",
            "initial_balance": 1000000
        })
        r2 = client.post("/api/v1/accounts/", json={
            "name": "계좌 B",
            "currency": "USD",
            "initial_balance": 500000
        })
        assert r1.status_code == 201
        assert r2.status_code == 201
        assert r1.json()["id"] != r2.json()["id"]
        assert r1.json()["currency"] == "KRW"
        assert r2.json()["currency"] == "USD"
