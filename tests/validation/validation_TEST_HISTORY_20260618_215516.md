# VALIDATION Test History

- **실행일시**: 2026-06-18 21:55:16
- **결과**: 19 passed / 1 failed / 20 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/validation/test_validation.py::TestValidation::test_account_empty_name | ✅ PASSED | 0.015 | 2026-06-18 21:55:07 |
| tests/validation/test_validation.py::TestValidation::test_account_negative_balance | ✅ PASSED | 0.009 | 2026-06-18 21:55:07 |
| tests/validation/test_validation.py::TestValidation::test_account_missing_currency | ✅ PASSED | 0.008 | 2026-06-18 21:55:08 |
| tests/validation/test_validation.py::TestValidation::test_account_valid_creation | ✅ PASSED | 0.037 | 2026-06-18 21:55:08 |
| tests/validation/test_validation.py::TestValidation::test_order_zero_quantity | ✅ PASSED | 0.006 | 2026-06-18 21:55:08 |
| tests/validation/test_validation.py::TestValidation::test_order_negative_quantity | ✅ PASSED | 0.007 | 2026-06-18 21:55:09 |
| tests/validation/test_validation.py::TestValidation::test_order_limit_no_price | ✅ PASSED | 0.01 | 2026-06-18 21:55:09 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_side | ✅ PASSED | 0.01 | 2026-06-18 21:55:10 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_type | ✅ PASSED | 0.005 | 2026-06-18 21:55:10 |
| tests/validation/test_validation.py::TestValidation::test_order_missing_symbol | ✅ PASSED | 0.006 | 2026-06-18 21:55:11 |
| tests/validation/test_validation.py::TestValidation::test_order_nonexistent_account | ✅ PASSED | 0.017 | 2026-06-18 21:55:11 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_limit | ✅ PASSED | 0.026 | 2026-06-18 21:55:12 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_market | ❌ FAILED | 0.017 | 2026-06-18 21:55:12 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_email | ✅ PASSED | 0.011 | 2026-06-18 21:55:13 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_password | ✅ PASSED | 0.011 | 2026-06-18 21:55:13 |
| tests/validation/test_validation.py::TestValidation::test_register_duplicate_username | ✅ PASSED | 0.079 | 2026-06-18 21:55:14 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_missing_agent_id | ✅ PASSED | 0.016 | 2026-06-18 21:55:14 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_valid | ✅ PASSED | 0.018 | 2026-06-18 21:55:14 |
| tests/validation/test_validation.py::TestValidation::test_security_event_missing_event_type | ✅ PASSED | 0.019 | 2026-06-18 21:55:15 |
| tests/validation/test_validation.py::TestValidation::test_security_event_valid | ✅ PASSED | 0.026 | 2026-06-18 21:55:16 |

---
*자동 생성: pytest sessionfinish hook*