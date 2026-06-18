# VALIDATION Test History

- **실행일시**: 2026-06-18 22:05:39
- **결과**: 20 passed / 0 failed / 20 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/validation/test_validation.py::TestValidation::test_account_empty_name | ✅ PASSED | 0.013 | 2026-06-18 22:04:59 |
| tests/validation/test_validation.py::TestValidation::test_account_negative_balance | ✅ PASSED | 0.004 | 2026-06-18 22:05:30 |
| tests/validation/test_validation.py::TestValidation::test_account_missing_currency | ✅ PASSED | 0.013 | 2026-06-18 22:05:30 |
| tests/validation/test_validation.py::TestValidation::test_account_valid_creation | ✅ PASSED | 0.03 | 2026-06-18 22:05:31 |
| tests/validation/test_validation.py::TestValidation::test_order_zero_quantity | ✅ PASSED | 0.004 | 2026-06-18 22:05:31 |
| tests/validation/test_validation.py::TestValidation::test_order_negative_quantity | ✅ PASSED | 0.017 | 2026-06-18 22:05:32 |
| tests/validation/test_validation.py::TestValidation::test_order_limit_no_price | ✅ PASSED | 0.01 | 2026-06-18 22:05:32 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_side | ✅ PASSED | 0.012 | 2026-06-18 22:05:33 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_type | ✅ PASSED | 0.012 | 2026-06-18 22:05:33 |
| tests/validation/test_validation.py::TestValidation::test_order_missing_symbol | ✅ PASSED | 0.008 | 2026-06-18 22:05:34 |
| tests/validation/test_validation.py::TestValidation::test_order_nonexistent_account | ✅ PASSED | 0.042 | 2026-06-18 22:05:34 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_limit | ✅ PASSED | 0.028 | 2026-06-18 22:05:35 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_market | ✅ PASSED | 0.022 | 2026-06-18 22:05:35 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_email | ✅ PASSED | 0.011 | 2026-06-18 22:05:36 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_password | ✅ PASSED | 0.012 | 2026-06-18 22:05:37 |
| tests/validation/test_validation.py::TestValidation::test_register_duplicate_username | ✅ PASSED | 0.067 | 2026-06-18 22:05:37 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_missing_agent_id | ✅ PASSED | 0.015 | 2026-06-18 22:05:38 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_valid | ✅ PASSED | 0.022 | 2026-06-18 22:05:38 |
| tests/validation/test_validation.py::TestValidation::test_security_event_missing_event_type | ✅ PASSED | 0.013 | 2026-06-18 22:05:39 |
| tests/validation/test_validation.py::TestValidation::test_security_event_valid | ✅ PASSED | 0.031 | 2026-06-18 22:05:39 |

---
*자동 생성: pytest sessionfinish hook*