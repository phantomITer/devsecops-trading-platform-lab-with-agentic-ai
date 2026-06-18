# SECURITY Test History

- **실행일시**: 2026-06-18 21:01:55
- **결과**: 12 passed / 2 failed / 14 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/security/test_security.py::TestSecurity::test_sql_injection_login_blocked | ✅ PASSED | 0.013 | 2026-06-18 21:00:27 |
| tests/security/test_security.py::TestSecurity::test_sql_injection_account_name_safe | ✅ PASSED | 0.031 | 2026-06-18 21:00:28 |
| tests/security/test_security.py::TestSecurity::test_fake_jwt_rejected | ✅ PASSED | 0.031 | 2026-06-18 21:00:28 |
| tests/security/test_security.py::TestSecurity::test_no_token_users_rejected | ✅ PASSED | 0.007 | 2026-06-18 21:00:29 |
| tests/security/test_security.py::TestSecurity::test_no_token_delete_rejected | ✅ PASSED | 0.004 | 2026-06-18 21:00:29 |
| tests/security/test_security.py::TestSecurity::test_very_long_name_handled | ❌ FAILED | 0.011 | 2026-06-18 21:00:31 |
| tests/security/test_security.py::TestSecurity::test_extreme_quantity_price_handled | ❌ FAILED | 0.016 | 2026-06-18 21:00:32 |
| tests/security/test_security.py::TestSecurity::test_xss_attempt_in_username | ✅ PASSED | 0.06 | 2026-06-18 21:00:32 |
| tests/security/test_security.py::TestSecurity::test_health_endpoint_responds | ✅ PASSED | 0.04 | 2026-06-18 21:00:32 |
| tests/security/test_security.py::TestSecurity::test_red_agent_attack_logged | ✅ PASSED | 0.018 | 2026-06-18 21:00:33 |
| tests/security/test_security.py::TestSecurity::test_blue_agent_detection_logged | ✅ PASSED | 0.036 | 2026-06-18 21:00:33 |
| tests/security/test_security.py::TestSecurity::test_security_events_retrievable | ✅ PASSED | 0.009 | 2026-06-18 21:00:34 |
| tests/test_v1.py::test_create_security_event | ✅ PASSED | 0.022 | 2026-06-18 21:01:26 |
| tests/test_v1.py::test_list_security_events | ✅ PASSED | 0.008 | 2026-06-18 21:01:27 |

---
*자동 생성: pytest sessionfinish hook*