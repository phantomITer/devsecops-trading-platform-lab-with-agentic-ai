# SMOKE Test History

- **실행일시**: 2026-06-18 22:01:40
- **결과**: 21 passed / 0 failed / 21 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/smoke/test_api_smoke.py::TestSmoke::test_health | ✅ PASSED | 0.004 | 2026-06-18 22:00:32 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_register | ✅ PASSED | 0.07 | 2026-06-18 22:00:32 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_login | ✅ PASSED | 0.103 | 2026-06-18 22:00:33 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_login_wrong_password | ✅ PASSED | 0.11 | 2026-06-18 22:00:33 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_account | ✅ PASSED | 0.014 | 2026-06-18 22:00:34 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_accounts | ✅ PASSED | 0.022 | 2026-06-18 22:00:34 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_account_by_id | ✅ PASSED | 0.015 | 2026-06-18 22:00:35 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_account_not_found | ✅ PASSED | 0.018 | 2026-06-18 22:00:35 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_account_negative_balance | ✅ PASSED | 0.01 | 2026-06-18 22:00:36 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order | ✅ PASSED | 0.075 | 2026-06-18 22:00:36 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_orders | ✅ PASSED | 0.012 | 2026-06-18 22:00:37 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_order_not_found | ✅ PASSED | 0.029 | 2026-06-18 22:00:37 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_zero_quantity | ✅ PASSED | 0.005 | 2026-06-18 22:00:38 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_limit_no_price | ✅ PASSED | 0.011 | 2026-06-18 22:00:38 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_invalid_account | ✅ PASSED | 0.008 | 2026-06-18 22:00:39 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_positions | ✅ PASSED | 0.015 | 2026-06-18 22:00:39 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_position_not_found | ✅ PASSED | 0.02 | 2026-06-18 22:00:40 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_agent_log | ✅ PASSED | 0.038 | 2026-06-18 22:00:40 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_agent_logs | ✅ PASSED | 0.007 | 2026-06-18 22:01:07 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_security_event | ✅ PASSED | 0.01 | 2026-06-18 22:01:08 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_security_events | ✅ PASSED | 0.005 | 2026-06-18 22:01:08 |

---
*자동 생성: pytest sessionfinish hook*