# Test History - smoke

- 실행 시각: 2026-06-16 22:48:08
- 파일: `test_api_smoke.py`
- 결과: 총 17개 | ✅ PASS 4개 | ❌ FAIL 13개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-16 | `test_api_smoke.py` | 17 | 4 | 13 |

## 상세 내용

- ✅ PASS GET /api/health → 200 → {'status': 'ok', 'app': 'DevSecOps Trading Platform', 'timestamp': '2026-06-16T22:48:08.588452'}
- ❌ FAIL POST /api/accounts → 201 → {'detail': 'Not Found'}
- ❌ FAIL GET /api/accounts → 200 → 1개
- ✅ PASS GET /api/accounts/9999 → 404
- ❌ FAIL POST /api/accounts (initial_balance=-1) → 4xx
- ❌ FAIL POST /api/orders → 201 → {'detail': 'Not Found'}
- ❌ FAIL GET /api/orders → 200 → 1개
- ✅ PASS GET /api/orders/9999 → 404
- ❌ FAIL POST /api/orders (quantity=-1) → 4xx
- ❌ FAIL POST /api/orders (LIMIT, price 없음) → 4xx
- ❌ FAIL POST /api/orders (account_id=9999) → 400
- ❌ FAIL GET /api/instruments → 200 → 1개
- ❌ FAIL GET /api/instruments?market=KOSPI → 200 → 1개
- ❌ FAIL GET /api/instruments?q=삼성 → 200 → 1개
- ❌ FAIL GET /api/instruments/AAPL → 200
- ❌ FAIL GET /api/instruments/aapl → 200 (대소문자 무시)
- ✅ PASS GET /api/instruments/XYZ → 404
