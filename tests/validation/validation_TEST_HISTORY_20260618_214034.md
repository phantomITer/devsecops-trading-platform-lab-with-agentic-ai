# VALIDATION Test History

- **실행일시**: 2026-06-18 21:40:34
- **결과**: 18 passed / 2 failed / 20 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/validation/test_validation.py::TestValidation::test_account_empty_name | ✅ PASSED | 0.009 | 2026-06-18 21:39:38 |
| tests/validation/test_validation.py::TestValidation::test_account_negative_balance | ✅ PASSED | 0.016 | 2026-06-18 21:39:39 |
| tests/validation/test_validation.py::TestValidation::test_account_missing_currency | ✅ PASSED | 0.01 | 2026-06-18 21:39:39 |
| tests/validation/test_validation.py::TestValidation::test_account_valid_creation | ✅ PASSED | 0.036 | 2026-06-18 21:39:40 |
| tests/validation/test_validation.py::TestValidation::test_order_zero_quantity | ✅ PASSED | 0.011 | 2026-06-18 21:39:40 |
| tests/validation/test_validation.py::TestValidation::test_order_negative_quantity | ✅ PASSED | 0.008 | 2026-06-18 21:39:41 |
| tests/validation/test_validation.py::TestValidation::test_order_limit_no_price | ✅ PASSED | 0.009 | 2026-06-18 21:40:02 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_side | ✅ PASSED | 0.008 | 2026-06-18 21:40:03 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_type | ✅ PASSED | 0.006 | 2026-06-18 21:40:04 |
| tests/validation/test_validation.py::TestValidation::test_order_missing_symbol | ✅ PASSED | 0.009 | 2026-06-18 21:40:04 |
| tests/validation/test_validation.py::TestValidation::test_order_nonexistent_account | ✅ PASSED | 0.018 | 2026-06-18 21:40:05 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_limit | ❌ FAILED | 0.049 | 2026-06-18 21:40:05 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_market | ❌ FAILED | 0.012 | 2026-06-18 21:40:06 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_email | ✅ PASSED | 0.01 | 2026-06-18 21:40:06 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_password | ✅ PASSED | 0.01 | 2026-06-18 21:40:07 |
| tests/validation/test_validation.py::TestValidation::test_register_duplicate_username | ✅ PASSED | 0.076 | 2026-06-18 21:40:07 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_missing_agent_id | ✅ PASSED | 0.014 | 2026-06-18 21:40:32 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_valid | ✅ PASSED | 0.031 | 2026-06-18 21:40:33 |
| tests/validation/test_validation.py::TestValidation::test_security_event_missing_event_type | ✅ PASSED | 0.014 | 2026-06-18 21:40:33 |
| tests/validation/test_validation.py::TestValidation::test_security_event_valid | ✅ PASSED | 0.019 | 2026-06-18 21:40:34 |

---
*자동 생성: pytest sessionfinish hook*