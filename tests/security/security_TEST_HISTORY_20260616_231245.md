# Test History - security

- 실행 시각: 2026-06-16 23:12:45
- 파일: `test_security.py`
- 결과: 총 12개 | ✅ PASS 12개 | ❌ FAIL 0개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-16 | `test_security.py` | 12 | 12 | 0 |

## 상세 내용

- ✅ PASS SQL Injection (symbol) → 서버 500 아님
- ✅ PASS XSS 시도 (name) → 서버 500 아님
- ✅ PASS quantity=999999999999 → 서버 500 아님
- ✅ PASS price=999999999999 → 서버 500 아님
- ✅ PASS initial_balance=999999999999 → 서버 500 아님
- ✅ PASS 빈 body → 4xx
- ✅ PASS 잘못된 JSON → 4xx
- ✅ PASS GET /api/nonexistent → 404
- ✅ PASS DELETE /api/accounts/1 → 405 (미구현)
- ✅ PASS account_id=abc → 422
- ✅ PASS quantity=abc → 422
- ✅ PASS initial_balance=abc → 422
