import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine


@pytest.fixture(autouse=True)
def reset_db():
    """각 테스트 전후 DB 초기화 (격리 보장)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """FastAPI TestClient 픽스처"""
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    """기본 테스트 유저 등록 픽스처"""
    r = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "password123"
    })
    assert r.status_code == 201
    return {"username": "testuser", "password": "password123"}


@pytest.fixture
def auth_token(client, registered_user):
    """로그인 후 JWT 토큰 반환 픽스처"""
    r = client.post("/api/v1/auth/login", json=registered_user)
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Authorization 헤더 픽스처"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_account(client):
    """테스트 계좌 생성 픽스처"""
    r = client.post("/api/v1/accounts/", json={
        "name": "테스트 계좌",
        "currency": "KRW",
        "initial_balance": 5000000
    })
    assert r.status_code == 201
    return r.json()
