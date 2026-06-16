# fix_validation_test.py
import re

with open("tests/validation/test_validation.py", "r", encoding="utf-8") as f:
    content = f.read()

# timestamp import 추가
old = "import requests"
new = "import requests\nimport time"
content = content.replace(old, new, 1)

# 계좌 생성 시 고유 이름 사용
old = '"name": "Validation Test Account"'
new = '"name": f"Validation-{int(time.time())}"'
content = content.replace(old, new, 1)

old = '"name": "Zero Balance"'
new = '"name": f"Zero-{int(time.time())}"'
content = content.replace(old, new, 1)

with open("tests/validation/test_validation.py", "w", encoding="utf-8") as f:
    f.write(content)
print("✅ test_validation.py 수정 완료")