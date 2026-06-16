# tests/utils/base.py
"""
전체 테스트 실행기 + 공통 유틸
실행: python tests/utils/base.py
     → 모든 테스트 모듈 순서대로 실행
     → 각 폴더에 {유형}_TEST_HISTORY_{YYYYMMDD_HHMMSS}.md 저장
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

PASS = "✅ PASS"
FAIL = "❌ FAIL"


# ──────────────────────────────────────────────
# 공통 유틸 함수
# ──────────────────────────────────────────────

def check(results: list, name: str, condition: bool, detail: str = ""):
    """테스트 결과 수집 + 콘솔 출력"""
    status = PASS if condition else FAIL
    results.append((status, name, detail))
    print(f"{status} {name}" + (f" → {detail}" if detail else ""))


def save_history(test_file: str, results: list):
    """
    테스트 결과를 해당 폴더에
    {유형}_TEST_HISTORY_{YYYYMMDD_HHMMSS}.md 로 저장
    """
    test_type = Path(test_file).parent.name
    now_dt = datetime.now()
    now_str = now_dt.strftime("%Y%m%d_%H%M%S")
    now_display = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    date = now_dt.strftime("%Y-%m-%d")

    filename = f"{test_type}_TEST_HISTORY_{now_str}.md"
    history_file = (
        Path(__file__).parent.parent
        / Path(test_file).parent
        / filename
    )

    passed = sum(1 for r in results if r[0] == PASS)
    failed = sum(1 for r in results if r[0] == FAIL)
    total = len(results)

    lines = []
    lines.append(f"# Test History - {test_type}")
    lines.append(f"")
    lines.append(f"- 실행 시각: {now_display}")
    lines.append(f"- 파일: `{Path(test_file).name}`")
    lines.append(f"- 결과: 총 {total}개 | {PASS} {passed}개 | {FAIL} {failed}개")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"| 날짜 | 파일 | 총 | PASS | FAIL |")
    lines.append(f"|------|------|----|------|------|")
    lines.append(f"| {date} | `{Path(test_file).name}` | {total} | {passed} | {failed} |")
    lines.append(f"")
    lines.append(f"## 상세 내용")
    lines.append(f"")
    for status, name, detail in results:
        lines.append(f"- {status} {name}" + (f" → {detail}" if detail else ""))
    lines.append("")

    with history_file.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n📝 이력 저장 → tests/{test_type}/{filename}")


def print_summary(results: list, test_name: str = ""):
    """결과 요약 콘솔 출력 + (passed, failed) 반환"""
    print("\n" + "=" * 60)
    print(f"결과 요약" + (f" - {test_name}" if test_name else ""))
    print("=" * 60)
    passed = sum(1 for r in results if r[0] == PASS)
    failed = sum(1 for r in results if r[0] == FAIL)
    print(f"총 {len(results)}개 테스트: {PASS} {passed}개 / {FAIL} {failed}개")
    if failed > 0:
        print("\n실패한 테스트:")
        for r in results:
            if r[0] == FAIL:
                print(f"  {r[0]} {r[1]}")
    print("=" * 60 + "\n")
    return passed, failed


# ──────────────────────────────────────────────
# 전체 테스트 실행기
# ──────────────────────────────────────────────

def run_all():
    from tests.smoke.test_api_smoke import run_tests as smoke
    from tests.validation.test_validation import run_tests as validation
    from tests.integration.test_integration import run_tests as integration
    from tests.security.test_security import run_tests as security
    from tests.e2e.test_e2e import run_tests as e2e

    test_modules = [
        ("Smoke",       smoke),
        ("Validation",  validation),
        ("Integration", integration),
        ("Security",    security),
        ("E2E",         e2e),
    ]

    total_passed = 0
    total_failed = 0

    print("\n" + "=" * 60)
    print("DevSecOps Trading Platform Lab - 전체 테스트 실행")
    print("=" * 60)

    for name, run_fn in test_modules:
        print(f"\n\n{'─' * 60}")
        print(f"▶ {name} 테스트 시작")
        print(f"{'─' * 60}")
        passed, failed = run_fn()
        total_passed += passed
        total_failed += failed

    print("\n" + "=" * 60)
    print("전체 테스트 최종 요약")
    print("=" * 60)
    print(f"총 {total_passed + total_failed}개 테스트")
    print(f"  {PASS} {total_passed}개")
    print(f"  {FAIL} {total_failed}개")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all()