# SMOKE Test History

- **실행일시**: 2026-06-18 21:01:55
- **결과**: 21 passed / 0 failed / 21 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/smoke/test_api_smoke.py::TestSmoke::test_health | ✅ PASSED | 0.003 | 2026-06-18 21:00:35 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_register | ✅ PASSED | 0.056 | 2026-06-18 21:00:35 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_login | ✅ PASSED | 0.094 | 2026-06-18 21:00:36 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_login_wrong_password | ✅ PASSED | 0.109 | 2026-06-18 21:00:36 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_account | ✅ PASSED | 0.035 | 2026-06-18 21:00:37 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_accounts | ✅ PASSED | 0.012 | 2026-06-18 21:00:37 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_account_by_id | ✅ PASSED | 0.006 | 2026-06-18 21:00:38 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_account_not_found | ✅ PASSED | 0.008 | 2026-06-18 21:00:38 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_account_negative_balance | ✅ PASSED | 0.006 | 2026-06-18 21:00:38 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order | ✅ PASSED | 0.025 | 2026-06-18 21:00:39 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_orders | ✅ PASSED | 0.006 | 2026-06-18 21:00:39 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_order_not_found | ✅ PASSED | 0.018 | 2026-06-18 21:00:40 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_zero_quantity | ✅ PASSED | 0.008 | 2026-06-18 21:00:41 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_limit_no_price | ✅ PASSED | 0.012 | 2026-06-18 21:00:42 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_invalid_account | ✅ PASSED | 0.022 | 2026-06-18 21:00:42 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_positions | ✅ PASSED | 0.018 | 2026-06-18 21:00:43 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_position_not_found | ✅ PASSED | 0.025 | 2026-06-18 21:00:43 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_agent_log | ✅ PASSED | 0.033 | 2026-06-18 21:00:44 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_agent_logs | ✅ PASSED | 0.013 | 2026-06-18 21:00:45 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_security_event | ✅ PASSED | 0.029 | 2026-06-18 21:00:46 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_security_events | ✅ PASSED | 0.01 | 2026-06-18 21:00:47 |

---
*자동 생성: pytest sessionfinish hook*