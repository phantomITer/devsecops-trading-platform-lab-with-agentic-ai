# fix_save_history.py
# 실행: python fix_save_history.py
from pathlib import Path

ROOT = Path(__file__).parent

# ── 파일별 설정 ──────────────────────────────────────────────────
TARGETS = [
    "tests/smoke/test_api_smoke.py",
    "tests/integration/test_integration.py",
    "tests/validation/test_validation.py",
    "tests/security/test_security.py",
    "tests/e2e/test_e2e.py",
]

LABELS = {
    "smoke":       "Smoke",
    "integration": "Integration",
    "validation":  "Validation",
    "security":    "Security",
    "e2e":         "E2E",
}

def fix(filepath: str):
    path = ROOT / filepath
    test_dir  = Path(filepath).parent.name          # e.g. "smoke"
    label     = LABELS[test_dir]
    hist_arg  = f"{test_dir}/{Path(filepath).name}" # e.g. "smoke/test_api_smoke.py"

    src = path.read_text(encoding="utf-8")

    # 1. import requests 다음 줄에 base import 추가 (중복 방지)
    if "from tests.utils.base import" not in src:
        src = src.replace(
            "import requests\n",
            "import requests\n"
            "from tests.utils.base import check as _chk, save_history, print_summary\n",
            1
        )

    # 2. 로컬 check 함수 + passed/failed 변수 블록 → _chk 래퍼로 교체
    #    두 가지 패턴 모두 처리 (results=[] 있는 것 / 없는 것)
    LOCAL_BLOCK_WITH_RESULTS = (
        "    results = []\n"
        "    passed = 0\n"
        "    failed = 0\n"
        "\n"
        "    def check(name, condition, detail=\"\"):\n"
        "        nonlocal passed, failed\n"
        "        if condition:\n"
        "            print(f\"  [PASS] {name}\")\n"
        "            passed += 1\n"
        "        else:\n"
        "            print(f\"  [FAIL] {name} | {detail}\")\n"
        "            failed += 1\n"
        "        results.append({\"name\": name, \"pass\": condition})\n"
    )
    LOCAL_BLOCK_NO_RESULTS = (
        "    passed = 0\n"
        "    failed = 0\n"
        "\n"
        "    def check(name, condition, detail=\"\"):\n"
        "        nonlocal passed, failed\n"
        "        if condition:\n"
        "            print(f\"  [PASS] {name}\")\n"
        "            passed += 1\n"
        "        else:\n"
        "            print(f\"  [FAIL] {name} | {detail}\")\n"
        "            failed += 1\n"
    )
    NEW_BLOCK = (
        "    results = []\n"
        "\n"
        "    def check(name, condition, detail=\"\"):\n"
        "        _chk(results, name, condition, detail)\n"
    )

    if LOCAL_BLOCK_WITH_RESULTS in src:
        src = src.replace(LOCAL_BLOCK_WITH_RESULTS, NEW_BLOCK)
    elif LOCAL_BLOCK_NO_RESULTS in src:
        src = src.replace(LOCAL_BLOCK_NO_RESULTS, NEW_BLOCK)
    else:
        print(f"  ⚠️  {filepath} — 로컬 check 블록 패턴 불일치")

    # 3. 마지막 print+return 블록 → print_summary + save_history + return 으로 교체
    #    기존: print("\n" + "=" * 60)
    #          print(f"결과: {passed} 통과 / ...")
    #          print("=" * 60)
    #          return passed, failed
    #    신규: passed, failed = print_summary(results, "Label")
    #          save_history("dir/file.py", results)
    #          return passed, failed

    import re
    src = re.sub(
        r'    print\("\\n" \+ "=" \* 60\)\n'
        r'    print\(f"[^\n]+"\)\n'
        r'    print\("=" \* 60\)\n'
        r'    return passed, failed',
        f'    passed, failed = print_summary(results, "{label}")\n'
        f'    save_history("{hist_arg}", results)\n'
        f'    return passed, failed',
        src
    )

    path.write_text(src, encoding="utf-8")
    print(f"  ✅ {filepath}")

print("\n" + "=" * 60)
print("fix_save_history.py")
print("=" * 60)
for t in TARGETS:
    print(f"\n▶ {t}")
    fix(t)

print("\n완료!")
print("python run_all_tests.py 로 확인하세요.")
print("히스토리 파일이 각 폴더에 생성됩니다.")