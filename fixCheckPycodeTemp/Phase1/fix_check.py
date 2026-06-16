# fix_check.py
content = '''from app.main import app
from fastapi.routing import APIRoute

for route in app.routes:
    if isinstance(route, APIRoute):
        print(route.methods, route.path)
'''

with open("check_routes.py", "w", encoding="utf-8") as f:
    f.write(content)
print("✅ check_routes.py 저장 완료")