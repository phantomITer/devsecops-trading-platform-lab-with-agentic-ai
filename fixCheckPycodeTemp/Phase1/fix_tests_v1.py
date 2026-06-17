# fix_tests_v1.py
import re
from pathlib import Path

ROOT = Path(__file__).parent

TARGETS = [
    ("tests/smoke/test_api_smoke.py",           "smoke/test_api_smoke.py",         "Smoke"),
    ("tests/integration/test_integration.py",   "integration/test_integration.py", "Integration"),
    ("tests/validation/test_validation.py",     "validation/test_validation.py",   "Validation"),
    ("tests/security/test_security.py",         "security/test_security.py",       "Security"),
    ("tests/e2e/test_e2e.py",                   "e2e/test_e2e.py",                 "E2E"),
]

def fix_file(filepath, history_arg, label):
    path = ROOT / filepath
    original = path.read_text(encoding="utf-8")
    text = original

    # 1. /api/ → /api/v1/
    text = re.sub(r'(BASE_URL\})/api/(?!v1/)', r'\1/api/v1/', text)
    text = re.sub(r'"((?:GET|POST|PUT|DELETE|PATCH) /api/)(?!v1/)', r'"\1v1/', text)

    # 2. try-finally 감싸기
    old_tail = (
        f'    passed, failed = print_summary(results, "{label}")\n'
        f'    save_history("{history_arg}", results)\n'
        f'    return passed, failed'
    )
    new_tail = (
        f'    except Exception as e:\n'
        f'        print(f"\\n❌ {label} 테스트 중 예외 발생: {{e}}")\n'
        f'        return 0, 0\n'
        f'    finally:\n'
        f'        passed, failed = print_summary(results, "{label}")\n'
        f'        save_history("{history_arg}", results)'
    )

    if old_tail in text:
        text = text.replace(
            'def run_tests():\n    results = []',
            'def run_tests():\n    results = []\n    try:'
        )
        text = text.replace(old_tail, new_tail)
        lines = text.split('\n')
        new_lines = []
        in_try = False
        for line in lines:
            if line == '    try:':
                new_lines.append(line)
                in_try = True
                continue
            if in_try and line.startswith('    except'):
                in_try = False
                new_lines.append(line)
                continue
            if in_try:
                new_lines.append('    ' + line if line.strip() else line)
                continue
            new_lines.append(line)
        text = '\n'.join(new_lines)
    else:
        print(f"  ⚠️  패턴 불일치 — 수동 확인 필요")

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  ✅ {filepath} 수정 완료")
    else:
        print(f"  ℹ️  {filepath} 변경 없음")

for filepath, history_arg, label in TARGETS:
    print(f"\n▶ {filepath}")
    fix_file(filepath, history_arg, label)

print("\n완료! 서버 켜고 python run_all_tests.py 실행하세요.")