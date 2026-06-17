# VALIDATION Test History

- **실행일시**: 2026-06-17 23:58:09
- **결과**: 20 passed / 0 failed / 20 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/validation/test_validation.py::TestValidation::test_account_empty_name | ✅ PASSED | 0.013 | 2026-06-17 23:57:37 |
| tests/validation/test_validation.py::TestValidation::test_account_negative_balance | ✅ PASSED | 0.014 | 2026-06-17 23:57:38 |
| tests/validation/test_validation.py::TestValidation::test_account_missing_currency | ✅ PASSED | 0.014 | 2026-06-17 23:57:40 |
| tests/validation/test_validation.py::TestValidation::test_account_valid_creation | ✅ PASSED | 0.109 | 2026-06-17 23:57:41 |
| tests/validation/test_validation.py::TestValidation::test_order_zero_quantity | ✅ PASSED | 0.005 | 2026-06-17 23:57:43 |
| tests/validation/test_validation.py::TestValidation::test_order_negative_quantity | ✅ PASSED | 0.008 | 2026-06-17 23:57:45 |
| tests/validation/test_validation.py::TestValidation::test_order_limit_no_price | ✅ PASSED | 0.008 | 2026-06-17 23:57:46 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_side | ✅ PASSED | 0.008 | 2026-06-17 23:57:48 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_type | ✅ PASSED | 0.004 | 2026-06-17 23:57:50 |
| tests/validation/test_validation.py::TestValidation::test_order_missing_symbol | ✅ PASSED | 0.008 | 2026-06-17 23:57:52 |
| tests/validation/test_validation.py::TestValidation::test_order_nonexistent_account | ✅ PASSED | 0.005 | 2026-06-17 23:57:53 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_limit | ✅ PASSED | 0.087 | 2026-06-17 23:57:55 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_market | ✅ PASSED | 0.082 | 2026-06-17 23:57:57 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_email | ✅ PASSED | 0.004 | 2026-06-17 23:57:58 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_password | ✅ PASSED | 0.003 | 2026-06-17 23:58:00 |
| tests/validation/test_validation.py::TestValidation::test_register_duplicate_username | ✅ PASSED | 0.125 | 2026-06-17 23:58:02 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_missing_agent_id | ✅ PASSED | 0.003 | 2026-06-17 23:58:03 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_valid | ✅ PASSED | 0.079 | 2026-06-17 23:58:05 |
| tests/validation/test_validation.py::TestValidation::test_security_event_missing_event_type | ✅ PASSED | 0.003 | 2026-06-17 23:58:07 |
| tests/validation/test_validation.py::TestValidation::test_security_event_valid | ✅ PASSED | 0.079 | 2026-06-17 23:58:08 |

---
*자동 생성: pytest sessionfinish hook*