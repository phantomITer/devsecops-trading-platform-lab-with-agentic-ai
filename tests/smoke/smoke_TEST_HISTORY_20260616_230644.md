# Test History - smoke

- 실행 시각: 2026-06-16 23:06:44
- 파일: `test_api_smoke.py`
- 결과: 총 19개 | ✅ PASS 19개 | ❌ FAIL 0개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-16 | `test_api_smoke.py` | 19 | 19 | 0 |

## 상세 내용

- ✅ PASS GET /api/health → 200 → {'status': 'ok', 'app': 'DevSecOps Trading Platform', 'timestamp': '2026-06-16T23:06:44.681450'}
- ✅ PASS POST /api/accounts → 201 → {'name': 'Test Account', 'currency': 'USD', 'id': 6, 'initial_balance': 10000.0, 'current_balance': 10000.0, 'created_at': '2026-06-16T14:06:44'}
- ✅ PASS GET /api/accounts → 200 → 6개
- ✅ PASS GET /api/accounts/6 → 200
- ✅ PASS GET /api/accounts/9999 → 404
- ✅ PASS POST /api/accounts (initial_balance=-1) → 4xx
- ✅ PASS POST /api/orders → 201 → {'account_id': 6, 'symbol': 'AAPL', 'side': 'BUY', 'type': 'MARKET', 'quantity': 10.0, 'price': 190.5, 'id': 1, 'status': 'NEW', 'created_at': '2026-06-16T14:06:44'}
- ✅ PASS GET /api/orders → 200 → 1개
- ✅ PASS GET /api/orders/1 → 200
- ✅ PASS GET /api/orders/9999 → 404
- ✅ PASS POST /api/orders (quantity=-1) → 4xx
- ✅ PASS POST /api/orders (LIMIT, price 없음) → 4xx
- ✅ PASS POST /api/orders (account_id=9999) → 400
- ✅ PASS GET /api/instruments → 200 → 10개
- ✅ PASS GET /api/instruments?market=KOSPI → 200 → 4개
- ✅ PASS GET /api/instruments?q=삼성 → 200 → 1개
- ✅ PASS GET /api/instruments/AAPL → 200
- ✅ PASS GET /api/instruments/aapl → 200 (대소문자 무시)
- ✅ PASS GET /api/instruments/XYZ → 404
