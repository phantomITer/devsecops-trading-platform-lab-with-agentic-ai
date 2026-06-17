# Test History - smoke

- 실행 시각: 2026-06-17 16:14:43
- 파일: `test_api_smoke.py`
- 결과: 총 22개 | ✅ PASS 21개 | ❌ FAIL 1개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-17 | `test_api_smoke.py` | 22 | 21 | 1 |

## 상세 내용

- ✅ PASS GET /api/v1/health/ → 200
- ❌ FAIL POST /api/v1/auth/register → 201 → {'detail': 'Username already exists'}
- ✅ PASS POST /api/v1/auth/login → 200
- ✅ PASS POST /api/v1/auth/login (wrong pw) → 401
- ✅ PASS POST /api/v1/accounts/ → 201 → {'id': 8, 'name': 'Smoke Account', 'currency': 'KRW', 'initial_balance': 1000000.0, 'current_balance': 1000000.0, 'created_at': '2026-06-17T07:14:43.460660'}
- ✅ PASS GET /api/v1/accounts/ → 200
- ✅ PASS GET /api/v1/accounts/8 → 200
- ✅ PASS GET /api/v1/accounts/9999 → 404
- ✅ PASS POST /api/v1/accounts/ (음수잔고) → 422
- ✅ PASS POST /api/v1/orders/ → 201
- ✅ PASS GET /api/v1/orders/ → 200
- ✅ PASS GET /api/v1/orders/7 → 200
- ✅ PASS GET /api/v1/orders/9999 → 404
- ✅ PASS POST /api/v1/orders/ (quantity=0) → 422
- ✅ PASS POST /api/v1/orders/ (LIMIT, price 없음) → 400
- ✅ PASS POST /api/v1/orders/ (없는 account) → 400
- ✅ PASS GET /api/v1/positions/ → 200
- ✅ PASS GET /api/v1/positions/9999 → 404
- ✅ PASS POST /api/v1/agent-logs/ → 201
- ✅ PASS GET /api/v1/agent-logs/ → 200
- ✅ PASS POST /api/v1/security-events/ → 201
- ✅ PASS GET /api/v1/security-events/ → 200
