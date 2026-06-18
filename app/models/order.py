from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    # 문자열 컬럼들에 길이 지정
    symbol = Column(String(20), nullable=False)          # 종목 코드 (ex. 005930)
    side = Column(String(4), nullable=False)             # BUY / SELL
    order_type = Column(String(10), nullable=False)      # MARKET / LIMIT
    status = Column(String(20), default="NEW")           # NEW / FILLED / CANCELED 등

    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    account = relationship("Account", back_populates="orders")