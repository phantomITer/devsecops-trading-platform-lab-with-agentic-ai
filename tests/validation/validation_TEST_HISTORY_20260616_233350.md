# Test History - validation

- 실행 시각: 2026-06-16 23:33:50
- 파일: `test_validation.py`
- 결과: 총 14개 | ✅ PASS 13개 | ❌ FAIL 1개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-16 | `test_validation.py` | 14 | 13 | 1 |

## 상세 내용

- ✅ PASS initial_balance=-1 → 4xx
- ❌ FAIL initial_balance=0 → 201 (허용)
- ✅ PASS name='' → 4xx
- ✅ PASS name 누락 → 422
- ✅ PASS currency 누락 → 422
- ✅ PASS quantity=0 → 4xx
- ✅ PASS quantity=-1 → 4xx
- ✅ PASS LIMIT price 없음 → 4xx
- ✅ PASS LIMIT price=0 → 4xx
- ✅ PASS LIMIT price=-1 → 4xx
- ✅ PASS MARKET price 있어도 → 201 (허용)
- ✅ PASS account_id=9999 → 400
- ✅ PASS side=INVALID → 4xx
- ✅ PASS type=INVALID → 4xx
