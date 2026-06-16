from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base

class OrderSide(str, enum.Enum):
    LONG  = "long"
    SHORT = "short"

class OrderStatus(str, enum.Enum):
    PENDING   = "pending"
    FILLED    = "filled"
    CANCELLED = "cancelled"
    REJECTED  = "rejected"

class Order(Base):
    __tablename__ = "orders"
    id           = Column(Integer, primary_key=True, index=True)
    agent_id     = Column(String, index=True, nullable=False)
    ticker       = Column(String, nullable=False)
    side         = Column(Enum(OrderSide), nullable=False)
    quantity     = Column(Integer, nullable=False)
    price        = Column(Float, nullable=True)
    filled_price = Column(Float, nullable=True)
    status       = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    reason       = Column(String, nullable=True)
    created_at   = Column(DateTime, server_default=func.now())
    filled_at    = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Order {self.agent_id} {self.side} {self.ticker} x{self.quantity}>"