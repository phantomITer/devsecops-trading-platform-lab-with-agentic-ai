# Test History - integration

- 실행 시각: 2026-06-16 23:28:51
- 파일: `test_integration.py`
- 결과: 총 15개 | ✅ PASS 15개 | ❌ FAIL 0개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-16 | `test_integration.py` | 15 | 15 | 0 |

## 상세 내용

- ✅ PASS 계좌 생성 → 201
- ✅ PASS 생성된 계좌가 목록에 포함
- ✅ PASS 생성된 계좌 단건 조회 → 200
- ✅ PASS 계좌 initial_balance = 50000
- ✅ PASS 계좌 current_balance = 50000
- ✅ PASS 주문 생성 → 201
- ✅ PASS 주문 account_id 일치
- ✅ PASS 주문 status = NEW
- ✅ PASS 생성된 주문이 목록에 포함
- ✅ PASS 생성된 주문 단건 조회 → 200
- ✅ PASS 주문 symbol = TSLA
- ✅ PASS 주문 quantity = 5.0
- ✅ PASS 주문 price = 250.0
- ✅ PASS 미국 주식 종목 목록 조회 → 200
- ✅ PASS 종목(AAPL)으로 주문 생성 → 201
