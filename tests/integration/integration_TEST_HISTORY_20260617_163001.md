# Test History - integration

- 실행 시각: 2026-06-17 16:30:01
- 파일: `test_integration.py`
- 결과: 총 14개 | ✅ PASS 13개 | ❌ FAIL 1개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-17 | `test_integration.py` | 14 | 13 | 1 |

## 상세 내용

- ❌ FAIL 회원가입 → 201
- ✅ PASS 로그인 → 200 + token
- ✅ PASS 계좌 생성 → 201
- ✅ PASS 계좌 단건 조회 → 200
- ✅ PASS 계좌 잔고 확인
- ✅ PASS 주문 생성 → 201
- ✅ PASS 주문 상태 NEW 확인
- ✅ PASS 주문 단건 조회 → 200
- ✅ PASS 주문 종목 확인
- ✅ PASS 없는 계좌로 주문 → 400
- ✅ PASS Agent Log 기록 → 201
- ✅ PASS Security Event 기록 → 201
- ✅ PASS Security Event 목록 조회 → 200
- ✅ PASS Security Event 존재 확인
