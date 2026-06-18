# SECURITY Test History

- **실행일시**: 2026-06-18 21:40:34
- **결과**: 14 passed / 0 failed / 14 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/security/test_security.py::TestSecurity::test_sql_injection_login_blocked | ✅ PASSED | 0.024 | 2026-06-18 21:38:10 |
| tests/security/test_security.py::TestSecurity::test_sql_injection_account_name_safe | ✅ PASSED | 0.034 | 2026-06-18 21:38:10 |
| tests/security/test_security.py::TestSecurity::test_fake_jwt_rejected | ✅ PASSED | 0.016 | 2026-06-18 21:38:11 |
| tests/security/test_security.py::TestSecurity::test_no_token_users_rejected | ✅ PASSED | 0.007 | 2026-06-18 21:38:11 |
| tests/security/test_security.py::TestSecurity::test_no_token_delete_rejected | ✅ PASSED | 0.014 | 2026-06-18 21:38:12 |
| tests/security/test_security.py::TestSecurity::test_very_long_name_handled | ✅ PASSED | 0.013 | 2026-06-18 21:38:12 |
| tests/security/test_security.py::TestSecurity::test_extreme_quantity_price_handled | ✅ PASSED | 0.019 | 2026-06-18 21:38:31 |
| tests/security/test_security.py::TestSecurity::test_xss_attempt_in_username | ✅ PASSED | 0.063 | 2026-06-18 21:38:32 |
| tests/security/test_security.py::TestSecurity::test_health_endpoint_responds | ✅ PASSED | 0.012 | 2026-06-18 21:38:32 |
| tests/security/test_security.py::TestSecurity::test_red_agent_attack_logged | ✅ PASSED | 0.028 | 2026-06-18 21:38:33 |
| tests/security/test_security.py::TestSecurity::test_blue_agent_detection_logged | ✅ PASSED | 0.027 | 2026-06-18 21:38:33 |
| tests/security/test_security.py::TestSecurity::test_security_events_retrievable | ✅ PASSED | 0.032 | 2026-06-18 21:38:34 |
| tests/test_v1.py::test_create_security_event | ✅ PASSED | 0.052 | 2026-06-18 21:39:37 |
| tests/test_v1.py::test_list_security_events | ✅ PASSED | 0.02 | 2026-06-18 21:39:37 |

---
*자동 생성: pytest sessionfinish hook*