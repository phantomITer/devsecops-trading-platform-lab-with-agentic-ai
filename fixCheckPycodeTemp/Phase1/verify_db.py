# verify_db.py
from app.database import SessionLocal
from app.models.accounts import Account
from app.models.orders import Order
from app.models.instruments import Instrument

db = SessionLocal()

print("=== 계좌 목록 ===")
for a in db.query(Account).all():
    print(f"  ID:{a.id} agent:{a.agent_id} 잔고:{a.balance:,.0f}원")

print("\n=== 주문 목록 ===")
for o in db.query(Order).all():
    print(f"  ID:{o.id} {o.agent_id} {o.side} {o.ticker} x{o.quantity}")

print("\n=== 종목 수 ===")
print(f"  {db.query(Instrument).count()}개")

db.close()