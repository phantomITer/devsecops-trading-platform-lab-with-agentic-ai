# INTEGRATION Test History

- **실행일시**: 2026-06-18 21:29:35
- **결과**: 6 passed / 1 failed / 7 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/integration/test_integration.py::TestIntegration::test_register_and_login_flow | ✅ PASSED | 0.124 | 2026-06-18 21:29:31 |
| tests/integration/test_integration.py::TestIntegration::test_account_create_and_retrieve | ✅ PASSED | 0.039 | 2026-06-18 21:29:32 |
| tests/integration/test_integration.py::TestIntegration::test_account_to_order_flow | ✅ PASSED | 0.043 | 2026-06-18 21:29:32 |
| tests/integration/test_integration.py::TestIntegration::test_order_invalid_account_returns_400 | ✅ PASSED | 0.012 | 2026-06-18 21:29:33 |
| tests/integration/test_integration.py::TestIntegration::test_agent_log_and_security_event_flow | ✅ PASSED | 0.065 | 2026-06-18 21:29:33 |
| tests/integration/test_integration.py::TestIntegration::test_full_order_pipeline | ❌ FAILED | 0.037 | 2026-06-18 21:29:34 |
| tests/integration/test_integration.py::TestIntegration::test_multiple_accounts_isolation | ✅ PASSED | 0.032 | 2026-06-18 21:29:35 |

---
*자동 생성: pytest sessionfinish hook*