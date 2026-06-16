from sqlalchemy.orm import Session
from app.models.orders import Order, OrderSide, OrderStatus
from typing import Optional
from datetime import datetime

def create_order(db: Session, agent_id: str, ticker: str, side: OrderSide,
                 quantity: int, price: Optional[float] = None, reason: Optional[str] = None) -> Order:
    order = Order(agent_id=agent_id, ticker=ticker, side=side,
                  quantity=quantity, price=price, reason=reason, status=OrderStatus.PENDING)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def fill_order(db: Session, order_id: int, filled_price: float) -> Optional[Order]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status       = OrderStatus.FILLED
    order.filled_price = filled_price
    order.filled_at    = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order

def get_orders_by_agent(db: Session, agent_id: str, limit: int = 50) -> list:
    return (db.query(Order).filter(Order.agent_id == agent_id)
            .order_by(Order.created_at.desc()).limit(limit).all())