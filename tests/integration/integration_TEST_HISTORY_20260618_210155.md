# INTEGRATION Test History

- **실행일시**: 2026-06-18 21:01:55
- **결과**: 6 passed / 2 failed / 8 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/integration/test_integration.py::TestIntegration::test_register_and_login_flow | ✅ PASSED | 0.103 | 2026-06-18 21:00:23 |
| tests/integration/test_integration.py::TestIntegration::test_account_create_and_retrieve | ✅ PASSED | 0.026 | 2026-06-18 21:00:24 |
| tests/integration/test_integration.py::TestIntegration::test_account_to_order_flow | ❌ FAILED | 0.042 | 2026-06-18 21:00:24 |
| tests/integration/test_integration.py::TestIntegration::test_order_invalid_account_returns_400 | ✅ PASSED | 0.021 | 2026-06-18 21:00:25 |
| tests/integration/test_integration.py::TestIntegration::test_agent_log_and_security_event_flow | ✅ PASSED | 0.073 | 2026-06-18 21:00:25 |
| tests/integration/test_integration.py::TestIntegration::test_full_order_pipeline | ❌ FAILED | 0.042 | 2026-06-18 21:00:26 |
| tests/integration/test_integration.py::TestIntegration::test_multiple_accounts_isolation | ✅ PASSED | 0.055 | 2026-06-18 21:00:27 |
| tests/test_phase2_agents.py::test_base_agent_llm_integration | ✅ PASSED | 0.0 | 2026-06-18 21:00:50 |

---
*자동 생성: pytest sessionfinish hook*