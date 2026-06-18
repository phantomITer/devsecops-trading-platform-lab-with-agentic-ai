# SECURITY Test History

- **실행일시**: 2026-06-18 21:19:15
- **결과**: 11 passed / 1 failed / 12 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/security/test_security.py::TestSecurity::test_sql_injection_login_blocked | ✅ PASSED | 0.073 | 2026-06-18 21:19:09 |
| tests/security/test_security.py::TestSecurity::test_sql_injection_account_name_safe | ✅ PASSED | 0.044 | 2026-06-18 21:19:09 |
| tests/security/test_security.py::TestSecurity::test_fake_jwt_rejected | ✅ PASSED | 0.007 | 2026-06-18 21:19:10 |
| tests/security/test_security.py::TestSecurity::test_no_token_users_rejected | ✅ PASSED | 0.008 | 2026-06-18 21:19:10 |
| tests/security/test_security.py::TestSecurity::test_no_token_delete_rejected | ✅ PASSED | 0.007 | 2026-06-18 21:19:10 |
| tests/security/test_security.py::TestSecurity::test_very_long_name_handled | ❌ FAILED | 0.01 | 2026-06-18 21:19:12 |
| tests/security/test_security.py::TestSecurity::test_extreme_quantity_price_handled | ✅ PASSED | 0.024 | 2026-06-18 21:19:12 |
| tests/security/test_security.py::TestSecurity::test_xss_attempt_in_username | ✅ PASSED | 0.074 | 2026-06-18 21:19:13 |
| tests/security/test_security.py::TestSecurity::test_health_endpoint_responds | ✅ PASSED | 0.008 | 2026-06-18 21:19:13 |
| tests/security/test_security.py::TestSecurity::test_red_agent_attack_logged | ✅ PASSED | 0.045 | 2026-06-18 21:19:14 |
| tests/security/test_security.py::TestSecurity::test_blue_agent_detection_logged | ✅ PASSED | 0.028 | 2026-06-18 21:19:14 |
| tests/security/test_security.py::TestSecurity::test_security_events_retrievable | ✅ PASSED | 0.021 | 2026-06-18 21:19:15 |

---
*자동 생성: pytest sessionfinish hook*