
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order
from app.models.account import Account
from app.schemas.order import OrderCreate

def create_order(db: Session, data: OrderCreate) -> Order:
    account = db.query(Account).filter(Account.id == data.account_id).first()
    if not account:
        raise HTTPException(status_code=400, detail=f"Account {data.account_id} does not exist")
    if data.order_type == "LIMIT" and (data.price is None or data.price <= 0):
        raise HTTPException(status_code=400, detail="Limit orders require a positive price")
    order = Order(
        account_id=data.account_id,
        symbol=data.symbol,
        side=data.side,
        order_type=data.order_type,
        quantity=data.quantity,
        price=data.price,
        status="NEW",
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders(db: Session):
    return db.query(Order).all()

def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
