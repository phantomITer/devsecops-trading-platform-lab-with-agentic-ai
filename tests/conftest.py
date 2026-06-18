import pytest
import json
from datetime import datetime
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine


# ──────────────────────────────────────────────
# DB 초기화
# ──────────────────────────────────────────────
@pytest.fixture(autouse=True)
def reset_db():
    """각 테스트 전후 DB 초기화 (격리 보장)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
#    Base.metadata.drop_all(bind=engine)


# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
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


# ──────────────────────────────────────────────
# 옵션 C - 자동 로그 저장 (기존 히스토리 포맷 유지)
# ──────────────────────────────────────────────
_session_results = []  # 세션 전체 결과 누적


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """각 테스트 결과를 캡처해서 누적"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        status = "PASSED" if report.passed else "FAILED"
        _session_results.append({
            "name": item.nodeid,
            "status": status,
            "duration": round(report.duration, 3),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })


def pytest_sessionfinish(session, exitstatus):
    """세션 종료 시 카테고리별 히스토리 .md 파일로 저장"""
    if not _session_results:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 카테고리 분류 키워드
    categories = {
        "smoke":      "tests/smoke",
        "validation": "tests/validation",
        "integration":"tests/integration",
        "security":   "tests/security",
        "e2e":        "tests/e2e",
        "phase2":     "tests",
        "v1":         "tests",
    }

    # 카테고리별 결과 분류
    buckets: dict[str, list] = {k: [] for k in categories}

    for r in _session_results:
        assigned = False
        for cat, _ in categories.items():
            if cat in r["name"].lower():
                buckets[cat].append(r)
                assigned = True
                break
        if not assigned:
            buckets["v1"].append(r)

    # 카테고리별 .md 저장
    for cat, results in buckets.items():
        if not results:
            continue

        save_dir = Path(categories[cat])
        save_dir.mkdir(parents=True, exist_ok=True)
        log_path = save_dir / f"{cat}_TEST_HISTORY_{timestamp}.md"

        passed = sum(1 for r in results if r["status"] == "PASSED")
        failed = sum(1 for r in results if r["status"] == "FAILED")
        total  = len(results)

        lines = [
            f"# {cat.upper()} Test History",
            f"",
            f"- **실행일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **결과**: {passed} passed / {failed} failed / {total} total",
            f"",
            f"| 테스트 | 결과 | 시간(s) | 타임스탬프 |",
            f"|--------|------|---------|------------|",
        ]

        for r in results:
            icon = "✅" if r["status"] == "PASSED" else "❌"
            lines.append(
                f"| {r['name']} | {icon} {r['status']} | {r['duration']} | {r['timestamp']} |"
            )

        lines += [
            f"",
            f"---",
            f"*자동 생성: pytest sessionfinish hook*",
        ]

        log_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"\n📄 로그 저장: {log_path}")