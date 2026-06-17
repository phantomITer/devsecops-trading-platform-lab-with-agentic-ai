import pytest


class TestSmoke:
    """Smoke Test - API 기본 동작 확인"""

    def test_health(self, client):
        """GET /api/v1/health/ 응답 200 확인"""
        r = client.get("/api/v1/health/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_register(self, client):
        """POST /api/v1/auth/register - 정상 등록 201"""
        r = client.post("/api/v1/auth/register", json={
            "username": "smokeuser",
            "email": "smoke@test.com",
            "password": "smoke1234"
        })
        assert r.status_code == 201

    def test_login(self, client):
        """POST /api/v1/auth/login - 정상 로그인 200"""
        client.post("/api/v1/auth/register", json={
            "username": "smokeuser",
            "email": "smoke@test.com",
            "password": "smoke1234"
        })
        r = client.post("/api/v1/auth/login", json={
            "username": "smokeuser",
            "password": "smoke1234"
        })
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_password(self, client):
        """POST /api/v1/auth/login - 잘못된 비밀번호 401"""
        client.post("/api/v1/auth/register", json={
            "username": "smokeuser",
            "email": "smoke@test.com",
            "password": "smoke1234"
        })
        r = client.post("/api/v1/auth/login", json={
            "username": "smokeuser",
            "password": "wrongpass"
        })
        assert r.status_code == 401

    def test_create_account(self, client):
        """POST /api/v1/accounts/ - 계좌 생성 201"""
        r = client.post("/api/v1/accounts/", json={
            "name": "Smoke Account",
            "currency": "KRW",
            "initial_balance": 1000000
        })
        assert r.status_code == 201

    def test_get_accounts(self, client):
        """GET /api/v1/accounts/ - 목록 조회 200"""
        r = client.get("/api/v1/accounts/")
        assert r.status_code == 200

    def test_get_account_by_id(self, client, test_account):
        """GET /api/v1/accounts/{id} - 단건 조회 200"""
        account_id = test_account["id"]
        r = client.get(f"/api/v1/accounts/{account_id}")
        assert r.status_code == 200

    def test_get_account_not_found(self, client):
        """GET /api/v1/accounts/9999 - 부재 시 404"""
        r = client.get("/api/v1/accounts/9999")
        assert r.status_code == 404

    def test_create_account_negative_balance(self, client):
        """POST /api/v1/accounts/ - 음수 잔고 422"""
        r = client.post("/api/v1/accounts/", json={
            "name": "Bad",
            "currency": "KRW",
            "initial_balance": -1
        })
        assert r.status_code == 422

    def test_create_order(self, client, test_account):
        """POST /api/v1/orders/ - 주문 생성 201"""
        r = client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "005930",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 10,
            "price": 75000
        })
        assert r.status_code == 201

    def test_get_orders(self, client):
        """GET /api/v1/orders/ - 목록 조회 200"""
        r = client.get("/api/v1/orders/")
        assert r.status_code == 200

    def test_get_order_not_found(self, client):
        """GET /api/v1/orders/9999 - 부재 시 404"""
        r = client.get("/api/v1/orders/9999")
        assert r.status_code == 404

    def test_create_order_zero_quantity(self, client, test_account):
        """POST /api/v1/orders/ - quantity=0 시 422"""
        r = client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "005930",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0
        })
        assert r.status_code == 422

    def test_create_order_limit_no_price(self, client, test_account):
        """POST /api/v1/orders/ - LIMIT 주문 price 없음 시 400"""
        r = client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "005930",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 10
        })
        assert r.status_code == 400

    def test_create_order_invalid_account(self, client):
        """POST /api/v1/orders/ - 존재하지 않는 account 시 400"""
        r = client.post("/api/v1/orders/", json={
            "account_id": 9999,
            "symbol": "005930",
            "side": "BUY",
            "order_type": "MARKET",
            "quantity": 10
        })
        assert r.status_code == 400

    def test_get_positions(self, client):
        """GET /api/v1/positions/ - 목록 조회 200"""
        r = client.get("/api/v1/positions/")
        assert r.status_code == 200

    def test_get_position_not_found(self, client):
        """GET /api/v1/positions/9999 - 부재 시 404"""
        r = client.get("/api/v1/positions/9999")
        assert r.status_code == 404

    def test_create_agent_log(self, client):
        """POST /api/v1/agent-logs/ - 에이전트 로그 생성 201"""
        r = client.post("/api/v1/agent-logs/", json={
            "agent_id": "red-smoke-001",
            "agent_type": "red",
            "action": "A03_SQL_INJECTION",
            "result": "simulated"
        })
        assert r.status_code == 201

    def test_get_agent_logs(self, client):
        """GET /api/v1/agent-logs/ - 목록 조회 200"""
        r = client.get("/api/v1/agent-logs/")
        assert r.status_code == 200

    def test_create_security_event(self, client):
        """POST /api/v1/security-events/ - 보안 이벤트 생성 201"""
        r = client.post("/api/v1/security-events/", json={
            "event_type": "ATTACK",
            "severity": "HIGH",
            "source": "red-agent",
            "description": "SQL Injection 탐지"
        })
        assert r.status_code == 201

    def test_get_security_events(self, client):
        """GET /api/v1/security-events/ - 목록 조회 200"""
        r = client.get("/api/v1/security-events/")
        assert r.status_code == 200
