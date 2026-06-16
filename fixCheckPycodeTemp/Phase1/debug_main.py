# debug_main.py
import traceback

try:
    from app.core.config import settings
    print("✅ config")
except Exception as e:
    print(f"❌ config: {e}")

try:
    from app.database import init_db
    print("✅ database")
except Exception as e:
    print(f"❌ database: {e}")

try:
    from app.api import health
    print("✅ health")
except Exception as e:
    print(f"❌ health: {e}")

try:
    from app.api import accounts
    print("✅ accounts")
except Exception as e:
    print(f"❌ accounts: {e}")

try:
    from app.api import orders
    print("✅ orders")
except Exception as e:
    print(f"❌ orders: {e}")

try:
    from app.api import instruments
    print("✅ instruments")
except Exception as e:
    print(f"❌ instruments: {e}")

try:
    from app.api.websocket import router as ws_router, market_broadcast_loop
    print("✅ websocket")
except Exception as e:
    print(f"❌ websocket: {e}")

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.api import health, accounts, orders, instruments
    from app.api.websocket import router as ws_router, market_broadcast_loop

    app = FastAPI()
    app.include_router(health.router,      prefix="/api")
    print("✅ health router included")
    app.include_router(accounts.router,    prefix="/api")
    print("✅ accounts router included")
    app.include_router(orders.router,      prefix="/api")
    print("✅ orders router included")
    app.include_router(instruments.router, prefix="/api")
    print("✅ instruments router included")
    app.include_router(ws_router)
    print("✅ websocket router included")

    from fastapi.routing import APIRoute
    routes = [r for r in app.routes if isinstance(r, APIRoute)]
    print(f"\n총 APIRoute: {len(routes)}개")
    for r in routes:
        print(f"  {r.methods} {r.path}")

except Exception as e:
    traceback.print_exc()

# debug_main.py 마지막 부분 교체
print("\n--- 실제 등록된 경로 ---")
for r in app.routes:
    if type(r).__name__ == '_IncludedRouter':
        router = r.original_router
        prefix = r.include_context.prefix if hasattr(r, 'include_context') else ''
        for route in router.routes:
            methods = getattr(route, 'methods', '?')
            path = getattr(route, 'path', '?')
            print(f"  {methods} {prefix}{path}")