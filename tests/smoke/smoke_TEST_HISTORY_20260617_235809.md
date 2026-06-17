# SMOKE Test History

- **실행일시**: 2026-06-17 23:58:09
- **결과**: 21 passed / 0 failed / 21 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/smoke/test_api_smoke.py::TestSmoke::test_health | ✅ PASSED | 0.003 | 2026-06-17 23:55:44 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_register | ✅ PASSED | 0.165 | 2026-06-17 23:55:46 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_login | ✅ PASSED | 0.175 | 2026-06-17 23:55:47 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_login_wrong_password | ✅ PASSED | 0.201 | 2026-06-17 23:55:49 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_account | ✅ PASSED | 0.086 | 2026-06-17 23:55:51 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_accounts | ✅ PASSED | 0.005 | 2026-06-17 23:55:53 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_account_by_id | ✅ PASSED | 0.004 | 2026-06-17 23:55:55 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_account_not_found | ✅ PASSED | 0.005 | 2026-06-17 23:55:56 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_account_negative_balance | ✅ PASSED | 0.005 | 2026-06-17 23:55:58 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order | ✅ PASSED | 0.079 | 2026-06-17 23:55:59 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_orders | ✅ PASSED | 0.004 | 2026-06-17 23:56:01 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_order_not_found | ✅ PASSED | 0.004 | 2026-06-17 23:56:02 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_zero_quantity | ✅ PASSED | 0.003 | 2026-06-17 23:56:04 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_limit_no_price | ✅ PASSED | 0.004 | 2026-06-17 23:56:06 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_order_invalid_account | ✅ PASSED | 0.005 | 2026-06-17 23:56:07 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_positions | ✅ PASSED | 0.004 | 2026-06-17 23:56:09 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_position_not_found | ✅ PASSED | 0.004 | 2026-06-17 23:56:10 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_agent_log | ✅ PASSED | 0.08 | 2026-06-17 23:56:12 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_agent_logs | ✅ PASSED | 0.008 | 2026-06-17 23:56:14 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_create_security_event | ✅ PASSED | 0.082 | 2026-06-17 23:56:15 |
| tests/smoke/test_api_smoke.py::TestSmoke::test_get_security_events | ✅ PASSED | 0.011 | 2026-06-17 23:56:17 |

---
*자동 생성: pytest sessionfinish hook*