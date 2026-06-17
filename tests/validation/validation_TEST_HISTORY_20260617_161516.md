# Test History - validation

- 실행 시각: 2026-06-17 16:15:16
- 파일: `test_validation.py`
- 결과: 총 12개 | ✅ PASS 12개 | ❌ FAIL 0개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-17 | `test_validation.py` | 12 | 12 | 0 |

## 상세 내용

- ✅ PASS 빈 name → 422
- ✅ PASS 음수 initial_balance → 422
- ✅ PASS initial_balance=0 → 201 (허용)
- ✅ PASS 잘못된 side(HOLD) → 422
- ✅ PASS 잘못된 order_type → 422
- ✅ PASS quantity=0 → 422
- ✅ PASS quantity 음수 → 422
- ✅ PASS LIMIT 주문 price 없음 → 400
- ✅ PASS 없는 account_id → 400
- ✅ PASS MARKET 주문 price 없어도 → 201
- ✅ PASS 빈 username → 422
- ✅ PASS 잘못된 email 형식 → 생성됨(422 아닐수있음)
