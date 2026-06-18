
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health():
    r = client.get("/api/v1/health/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register():
    r = client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    assert r.status_code == 201

def test_register_duplicate():
    client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    r = client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    assert r.status_code == 400

def test_login():
    client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    r = client.post("/api/v1/auth/login", json={
        "username": "testuser", "password": "password123"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_wrong_password():
    client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    r = client.post("/api/v1/auth/login", json={
        "username": "testuser", "password": "wrongpass"
    })
    assert r.status_code == 401

def test_create_account():
    r = client.post("/api/v1/accounts/", json={
        "name": "Test Account", "currency": "KRW", "initial_balance": 1000000
    })
    assert r.status_code == 201

def test_create_account_negative_balance():
    r = client.post("/api/v1/accounts/", json={
        "name": "Test", "currency": "KRW", "initial_balance": -1000
    })
    assert r.status_code == 422

def test_create_account_empty_name():
    r = client.post("/api/v1/accounts/", json={
        "name": "", "currency": "KRW", "initial_balance": 1000
    })
    assert r.status_code == 422

def test_list_accounts():
    client.post("/api/v1/accounts/", json={
        "name": "Account A", "currency": "KRW", "initial_balance": 500000
    })
    r = client.get("/api/v1/accounts/")
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_get_account_not_found():
    r = client.get("/api/v1/accounts/9999")
    assert r.status_code == 404

def test_create_order():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    assert r.status_code == 201

def test_create_order_invalid_account():
    r = client.post("/api/v1/orders/", json={
        "account_id": 9999,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    assert r.status_code == 400

def test_create_order_limit_no_price():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10
    })
    assert r.status_code == 400

def test_create_order_zero_quantity():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 0
    })
    assert r.status_code == 422

def test_create_order_invalid_side():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "HOLD",
        "order_type": "MARKET",
        "quantity": 10
    })
    assert r.status_code == 422

def test_list_orders():
    r = client.get("/api/v1/orders/")
    assert r.status_code == 200

def test_get_order_not_found():
    r = client.get("/api/v1/orders/9999")
    assert r.status_code == 404

def test_list_positions():
    r = client.get("/api/v1/positions/")
    assert r.status_code == 200

def test_get_position_not_found():
    r = client.get("/api/v1/positions/9999")
    assert r.status_code == 404

def test_create_agent_log():
    r = client.post("/api/v1/agent-logs/", json={
        "agent_id": "red-001",
        "agent_type": "red",
        "action": "A03_SQL_INJECTION",
        "result": "success"
    })
    assert r.status_code == 201

def test_list_agent_logs():
    r = client.get("/api/v1/agent-logs/")
    assert r.status_code == 200

def test_create_security_event():
    r = client.post("/api/v1/security-events/", json={
        "event_type": "ATTACK",
        "severity": "HIGH",
        "source": "red-agent",
        "description": "SQL Injection detected"
    })
    assert r.status_code == 201

def test_list_security_events():
    r = client.get("/api/v1/security-events/")
    assert r.status_code == 200

def test_e2e_full_flow(client):
    # 1) 회원가입
    r = client.post("/api/v1/auth/register", json={
        "username": "v1e2e",
        "email": "v1e2e@test.com",
        "password": "v1e2e1234",
    })
    assert r.status_code == 201

    # 2) 로그인
    r = client.post("/api/v1/auth/login", json={
        "username": "v1e2e",
        "password": "v1e2e1234",
    })
    assert r.status_code == 200
    assert "access_token" in r.json()

    # 3) 계좌 생성
    r = client.post("/api/v1/accounts/", json={
        "name": "v1 E2E 계좌",
        "currency": "KRW",
        "initial_balance": 5_000_000,
    })
    assert r.status_code == 201
    account_id = r.json()["id"]

    # 4) 주문 (BUY LIMIT, 즉시 체결 기대)
    r = client.post("/api/v1/orders/", json={
        "account_id": account_id,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 5,
        "price": 75_000,
    })
    assert r.status_code == 201
    assert r.json()["status"] == "FILLED"
