
import sys
from tests.smoke.test_api_smoke import run_tests as smoke
from tests.integration.test_integration import run_tests as integration
from tests.validation.test_validation import run_tests as validation
from tests.security.test_security import run_tests as security
from tests.e2e.test_e2e import run_tests as e2e

total_passed = 0
total_failed = 0

print("\n" + "=" * 60)
print("전체 테스트 실행")
print("=" * 60)

for name, fn in [
    ("Smoke", smoke),
    ("Integration", integration),
    ("Validation", validation),
    ("Security", security),
    ("E2E", e2e),
]:
    p, f = fn()
    total_passed += p
    total_failed += f

print("\n" + "=" * 60)
print(f"최종 결과: {total_passed} 통과 / {total_passed + total_failed} 전체")
if total_failed == 0:
    print("✅ 전체 통과!")
else:
    print(f"❌ {total_failed}개 실패")
print("=" * 60)
