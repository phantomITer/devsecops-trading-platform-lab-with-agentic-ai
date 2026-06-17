# SECURITY Test History

- **실행일시**: 2026-06-17 23:58:09
- **결과**: 14 passed / 0 failed / 14 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/security/test_security.py::TestSecurity::test_sql_injection_login_blocked | ✅ PASSED | 0.004 | 2026-06-17 23:55:25 |
| tests/security/test_security.py::TestSecurity::test_sql_injection_account_name_safe | ✅ PASSED | 0.08 | 2026-06-17 23:55:26 |
| tests/security/test_security.py::TestSecurity::test_fake_jwt_rejected | ✅ PASSED | 0.007 | 2026-06-17 23:55:28 |
| tests/security/test_security.py::TestSecurity::test_no_token_users_rejected | ✅ PASSED | 0.003 | 2026-06-17 23:55:29 |
| tests/security/test_security.py::TestSecurity::test_no_token_delete_rejected | ✅ PASSED | 0.004 | 2026-06-17 23:55:31 |
| tests/security/test_security.py::TestSecurity::test_very_long_name_handled | ✅ PASSED | 0.079 | 2026-06-17 23:55:32 |
| tests/security/test_security.py::TestSecurity::test_extreme_quantity_price_handled | ✅ PASSED | 0.078 | 2026-06-17 23:55:34 |
| tests/security/test_security.py::TestSecurity::test_xss_attempt_in_username | ✅ PASSED | 0.114 | 2026-06-17 23:55:36 |
| tests/security/test_security.py::TestSecurity::test_health_endpoint_responds | ✅ PASSED | 0.003 | 2026-06-17 23:55:37 |
| tests/security/test_security.py::TestSecurity::test_red_agent_attack_logged | ✅ PASSED | 0.09 | 2026-06-17 23:55:39 |
| tests/security/test_security.py::TestSecurity::test_blue_agent_detection_logged | ✅ PASSED | 0.081 | 2026-06-17 23:55:41 |
| tests/security/test_security.py::TestSecurity::test_security_events_retrievable | ✅ PASSED | 0.005 | 2026-06-17 23:55:42 |
| tests/test_v1.py::test_create_security_event | ✅ PASSED | 0.098 | 2026-06-17 23:57:31 |
| tests/test_v1.py::test_list_security_events | ✅ PASSED | 0.012 | 2026-06-17 23:57:33 |

---
*자동 생성: pytest sessionfinish hook*