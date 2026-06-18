# VALIDATION Test History

- **실행일시**: 2026-06-18 21:01:55
- **결과**: 18 passed / 2 failed / 20 total

| 테스트 | 결과 | 시간(s) | 타임스탬프 |
|--------|------|---------|------------|
| tests/validation/test_validation.py::TestValidation::test_account_empty_name | ✅ PASSED | 0.004 | 2026-06-18 21:01:28 |
| tests/validation/test_validation.py::TestValidation::test_account_negative_balance | ✅ PASSED | 0.004 | 2026-06-18 21:01:28 |
| tests/validation/test_validation.py::TestValidation::test_account_missing_currency | ✅ PASSED | 0.003 | 2026-06-18 21:01:29 |
| tests/validation/test_validation.py::TestValidation::test_account_valid_creation | ✅ PASSED | 0.011 | 2026-06-18 21:01:29 |
| tests/validation/test_validation.py::TestValidation::test_order_zero_quantity | ✅ PASSED | 0.004 | 2026-06-18 21:01:46 |
| tests/validation/test_validation.py::TestValidation::test_order_negative_quantity | ✅ PASSED | 0.01 | 2026-06-18 21:01:47 |
| tests/validation/test_validation.py::TestValidation::test_order_limit_no_price | ✅ PASSED | 0.02 | 2026-06-18 21:01:47 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_side | ✅ PASSED | 0.006 | 2026-06-18 21:01:48 |
| tests/validation/test_validation.py::TestValidation::test_order_invalid_type | ✅ PASSED | 0.003 | 2026-06-18 21:01:49 |
| tests/validation/test_validation.py::TestValidation::test_order_missing_symbol | ✅ PASSED | 0.004 | 2026-06-18 21:01:49 |
| tests/validation/test_validation.py::TestValidation::test_order_nonexistent_account | ✅ PASSED | 0.011 | 2026-06-18 21:01:50 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_limit | ❌ FAILED | 0.026 | 2026-06-18 21:01:50 |
| tests/validation/test_validation.py::TestValidation::test_order_valid_market | ❌ FAILED | 0.027 | 2026-06-18 21:01:51 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_email | ✅ PASSED | 0.012 | 2026-06-18 21:01:52 |
| tests/validation/test_validation.py::TestValidation::test_register_missing_password | ✅ PASSED | 0.004 | 2026-06-18 21:01:52 |
| tests/validation/test_validation.py::TestValidation::test_register_duplicate_username | ✅ PASSED | 0.087 | 2026-06-18 21:01:53 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_missing_agent_id | ✅ PASSED | 0.01 | 2026-06-18 21:01:53 |
| tests/validation/test_validation.py::TestValidation::test_agent_log_valid | ✅ PASSED | 0.016 | 2026-06-18 21:01:54 |
| tests/validation/test_validation.py::TestValidation::test_security_event_missing_event_type | ✅ PASSED | 0.012 | 2026-06-18 21:01:55 |
| tests/validation/test_validation.py::TestValidation::test_security_event_valid | ✅ PASSED | 0.028 | 2026-06-18 21:01:55 |

---
*자동 생성: pytest sessionfinish hook*