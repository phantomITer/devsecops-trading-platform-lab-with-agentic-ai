# SECURITY Test History

- **실행일시**: 2026-06-18 21:23:35
- **결과**: 12 passed / 0 failed / 12 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/security/test_security.py::TestSecurity::test_sql_injection_login_blocked | ✅ PASSED | 0.031 | 2026-06-18 21:23:29 |
| tests/security/test_security.py::TestSecurity::test_sql_injection_account_name_safe | ✅ PASSED | 0.035 | 2026-06-18 21:23:29 |
| tests/security/test_security.py::TestSecurity::test_fake_jwt_rejected | ✅ PASSED | 0.016 | 2026-06-18 21:23:30 |
| tests/security/test_security.py::TestSecurity::test_no_token_users_rejected | ✅ PASSED | 0.008 | 2026-06-18 21:23:31 |
| tests/security/test_security.py::TestSecurity::test_no_token_delete_rejected | ✅ PASSED | 0.009 | 2026-06-18 21:23:31 |
| tests/security/test_security.py::TestSecurity::test_very_long_name_handled | ✅ PASSED | 0.006 | 2026-06-18 21:23:32 |
| tests/security/test_security.py::TestSecurity::test_extreme_quantity_price_handled | ✅ PASSED | 0.021 | 2026-06-18 21:23:32 |
| tests/security/test_security.py::TestSecurity::test_xss_attempt_in_username | ✅ PASSED | 0.074 | 2026-06-18 21:23:33 |
| tests/security/test_security.py::TestSecurity::test_health_endpoint_responds | ✅ PASSED | 0.014 | 2026-06-18 21:23:33 |
| tests/security/test_security.py::TestSecurity::test_red_agent_attack_logged | ✅ PASSED | 0.037 | 2026-06-18 21:23:34 |
| tests/security/test_security.py::TestSecurity::test_blue_agent_detection_logged | ✅ PASSED | 0.053 | 2026-06-18 21:23:35 |
| tests/security/test_security.py::TestSecurity::test_security_events_retrievable | ✅ PASSED | 0.012 | 2026-06-18 21:23:35 |

---
*자동 생성: pytest sessionfinish hook*