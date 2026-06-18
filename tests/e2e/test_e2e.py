import pytest


class TestE2E:
    """E2E Test - 전체 시스템 시나리오 End-to-End 테스트"""

    def test_full_user_trading_flow(self, client):
        """회원가입 → 로그인 → 계좌 → 주문 전체 흐름"""
        # 1. 회원가입
        r = client.post("/api/v1/auth/register", json={
            "username": "e2euser",
            "email": "e2e@test.com",
            "password": "e2e1234"
        })
        assert r.status_code == 201

        # 2. 로그인
        r = client.post("/api/v1/auth/login", json={
            "username": "e2euser",
            "password": "e2e1234"
        })
        assert r.status_code == 200
        assert "access_token" in r.json()
        token = r.json()["access_token"]

        # 3. 계좌 생성
        r = client.post("/api/v1/accounts/", json={
            "name": "E2E 모의계좌",
            "currency": "KRW",
            "initial_balance": 10_000_000
        })
        assert r.status_code == 201
        account_id = r.json()["id"]

        # 4. 계좌 조회 + 잔고 확인
        r = client.get(f"/api/v1/accounts/{account_id}")
        assert r.status_code == 200
        assert r.json()["current_balance"] == 10_000_000

        # 5. 매수 주문 (BUY LIMIT)
        r = client.post("/api/v1/orders/", json={
            "account_id": account_id,
            "symbol": "005930",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 10,
            "price": 75_000
        })
        assert r.status_code == 201
        assert r.json()["status"] == "FILLED"

        # 6. 매도 주문 (SELL MARKET, 보유 수량 이내 + 가격 명시)
        r = client.post("/api/v1/orders/", json={
            "account_id": account_id,
            "symbol": "005930",
            "side": "SELL",
            "order_type": "MARKET",
            "quantity": 5,
            "price": 80_000,
        })
        assert r.status_code == 201
        assert r.json()["status"] == "FILLED"

        # 7. 주문 목록 확인
        r = client.get("/api/v1/orders/")
        assert r.status_code == 200
        assert len(r.json()) >= 2

    def test_red_blue_agent_scenario(self, client):
        """Red Agent 공격 → Blue Agent 탐지 시나리오"""
        # Red Agent 공격 로그
        r = client.post("/api/v1/agent-logs/", json={
            "agent_id": "red-e2e-001",
            "agent_type": "red",
            "action": "A03_SQL_INJECTION",
            "result": "공격 시도"
        })
        assert r.status_code == 201

        # Blue Agent 보안 이벤트 기록
        r = client.post("/api/v1/security-events/", json={
            "event_type": "ATTACK",
            "severity": "HIGH",
            "source": "red-e2e-001",
            "description": "SQL Injection 탐지 및 차단"
        })
        assert r.status_code == 201

        # 전체 보안이벤트 확인
        r = client.get("/api/v1/security-events/")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_multi_symbol_order_flow(self, client, test_account):
        """복수 종목 주문 흐름 E2E"""
        symbols = ["005930", "035420", "000660"]
        for symbol in symbols:
            r = client.post("/api/v1/orders/", json={
                "account_id": test_account["id"],
                "symbol": symbol,
                "side": "BUY",
                "order_type": "LIMIT",
                "quantity": 5,
                "price": 50_000
            })
            assert r.status_code == 201

        # 주문 목록 조회
        r = client.get("/api/v1/orders/")
        assert r.status_code == 200
        assert len(r.json()) >= 3

    def test_positions_after_orders(self, client, test_account):
        """주문 후 포지션 조회"""
        # 주문 생성
        client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "005930",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 10,
            "price": 75_000
        })

        # 포지션 목록 조회
        r = client.get("/api/v1/positions/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_complete_devsecops_flow(self, client):
        """DevSecOps 전체 파이프라인 E2E"""
        # 개발: 계좌 생성
        r = client.post("/api/v1/accounts/", json={
            "name": "DevSecOps 테스트",
            "currency": "KRW",
            "initial_balance": 50_000_000
        })
        assert r.status_code == 201
        account_id = r.json()["id"]

        # 보안: Red Agent 취약점 스캔
        r = client.post("/api/v1/agent-logs/", json={
            "agent_id": "red-devsecops-001",
            "agent_type": "red",
            "action": "A01_BROKEN_ACCESS",
            "result": "취약점 탐색"
        })
        assert r.status_code == 201

        # 보안: Blue Agent 탐지
        r = client.post("/api/v1/security-events/", json={
            "event_type": "ANOMALY",
            "severity": "CRITICAL",
            "source": "red-devsecops-001",
            "description": "Broken Access Control 시도 탐지"
        })
        assert r.status_code == 201

        # 운영: 주문 실행 (BUY MARKET, price 명시)
        r = client.post("/api/v1/orders/", json={
            "account_id": account_id,
            "symbol": "005930",
            "side": "BUY",
            "order_type": "MARKET",
            "quantity": 100,
            "price": 75_000,
        })
        assert r.status_code == 201
        assert r.json()["status"] == "FILLED"

        # 전체 상태 확인
        assert client.get("/api/v1/accounts/").status_code == 200
        assert client.get("/api/v1/orders/").status_code == 200
        assert client.get("/api/v1/security-events/").status_code == 200
        assert client.get("/api/v1/agent-logs/").status_code == 200