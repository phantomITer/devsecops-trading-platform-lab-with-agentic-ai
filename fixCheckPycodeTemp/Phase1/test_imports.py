# test_imports.py

try:
    from app.core.config import settings
    print("✅ config OK:", settings.APP_NAME)
except Exception as e:
    print("❌ config FAIL:", e)

try:
    from app.core.security import verify_api_key
    print("✅ security OK")
except Exception as e:
    print("❌ security FAIL:", e)

try:
    from app.core.dependencies import get_db
    print("✅ dependencies OK")
except Exception as e:
    print("❌ dependencies FAIL:", e)

try:
    from app.database import init_db
    print("✅ database OK")
except Exception as e:
    print("❌ database FAIL:", e)

try:
    from app.models import Account, Order, Instrument
    print("✅ models OK")
except Exception as e:
    print("❌ models FAIL:", e)

try:
    from app.services.accountsservice import init_all_accounts
    print("✅ accountsservice OK")
except Exception as e:
    print("❌ accountsservice FAIL:", e)

try:
    from app.services.ordersservice import create_order
    print("✅ ordersservice OK")
except Exception as e:
    print("❌ ordersservice FAIL:", e)

try:
    from app.adapters.krx_fetcher import get_current_price
    print("✅ krx_fetcher OK")
except Exception as e:
    print("❌ krx_fetcher FAIL:", e)

try:
    from app.adapters.mock_generator import get_mock_market_snapshot
    print("✅ mock_generator OK")
except Exception as e:
    print("❌ mock_generator FAIL:", e)

try:
    from app.api.websocket import router
    print("✅ websocket OK")
except Exception as e:
    print("❌ websocket FAIL:", e)

print("\n--- 완료 ---")