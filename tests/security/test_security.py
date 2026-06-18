import pytest


class TestSecurity:
    """Security Test - OWASP Top10 보안 시나리오 시뮬레이션"""

    # ===== SQL Injection =====

    def test_sql_injection_login_blocked(self, client):
        """SQL Injection 로그인 시도 401 차단"""
        r = client.post("/api/v1/auth/login", json={
            "username": "admin' OR '1'='1",
            "password": "anything"
        })
        assert r.status_code == 401

    def test_sql_injection_account_name_safe(self, client):
        """SQL Injection 계좌명 안전하게 저장 201"""
        r = client.post("/api/v1/accounts/", json={
            "name": "'; DROP TABLE accounts; --",
            "currency": "KRW",
            "initial_balance": 1000
        })
        assert r.status_code == 201

    # ===== 인증 우회 (Broken Access Control) =====

    def test_fake_jwt_rejected(self, client):
        """위조 JWT 토큰 401 거부"""
        r = client.get("/api/v1/users/", headers={
            "Authorization": "Bearer fakejwttoken"
        })
        assert r.status_code == 401

    def test_no_token_users_rejected(self, client):
        """토큰 없이 users 접근 401"""
        r = client.get("/api/v1/users/")
        assert r.status_code == 401

    def test_no_token_delete_rejected(self, client):
        """토큰 없이 DELETE 401"""
        r = client.delete("/api/v1/users/1")
        assert r.status_code == 401

    # ===== 비정상 입력값 =====

    def test_very_long_name_handled(self, client):
        """매우 긴 name 입력 처리"""
        r = client.post("/api/v1/accounts/", json={
            "name": "A" * 10000,
            "currency": "KRW",
            "initial_balance": 1000
        })
        assert r.status_code in (400, 422)

    def test_extreme_quantity_price_handled(self, client, test_account):
        """극단적 수량/가격 주문 처리"""
        r = client.post("/api/v1/orders/", json={
            "account_id": test_account["id"],
            "symbol": "005930",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 999999999,
            "price": 999999999
        })
        assert r.status_code in (400, 422)

    def test_xss_attempt_in_username(self, client):
        """XSS 시도 username 안전하게 처리"""
        r = client.post("/api/v1/auth/register", json={
            "username": "<script>alert(1)</script>",
            "email": "xss@test.com",
            "password": "test1234"
        })
        assert r.status_code in (201, 422)

    # ===== 보안 헤더 =====

    def test_health_endpoint_responds(self, client):
        """서비스 정상 응답 확인"""
        r = client.get("/api/v1/health/")
        assert r.status_code == 200

    # ===== 에이전트 보안 로깅 =====

    def test_red_agent_attack_logged(self, client):
        """Red Agent 공격 시뮬레이션 로깅"""
        r = client.post("/api/v1/agent-logs/", json={
            "agent_id": "red-sec-001",
            "agent_type": "red",
            "action": "A03_SQL_INJECTION",
            "result": "공격 시도"
        })
        assert r.status_code == 201

    def test_blue_agent_detection_logged(self, client):
        """Blue Agent 탐지 이벤트 로깅"""
        r = client.post("/api/v1/security-events/", json={
            "event_type": "ATTACK",
            "severity": "HIGH",
            "source": "red-sec-001",
            "description": "SQL Injection 탐지 및 차단"
        })
        assert r.status_code == 201

    def test_security_events_retrievable(self, client):
        """Security Event 목록 조회"""
        r = client.get("/api/v1/security-events/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)
