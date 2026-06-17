# Test History - security

- 실행 시각: 2026-06-17 16:14:45
- 파일: `test_security.py`
- 결과: 총 9개 | ✅ PASS 8개 | ❌ FAIL 1개

---

| 날짜 | 파일 | 총 | PASS | FAIL |
|------|------|----|------|------|
| 2026-06-17 | `test_security.py` | 9 | 8 | 1 |

## 상세 내용

- ✅ PASS SQL Injection 로그인 → 401 차단
- ✅ PASS SQL Injection 계좌명 → 201 (안전하게 저장)
- ✅ PASS 위조 JWT → 401
- ✅ PASS 토큰 없이 users 접근 → 401
- ✅ PASS 토큰 없이 DELETE → 401
- ✅ PASS 매우 긴 name → 처리됨 (201 or 422)
- ✅ PASS 극단적 수량/가격 → 처리됨 (201 or 422)
- ❌ FAIL XSS 시도 username → 처리됨
- ✅ PASS 서버 응답 정상
