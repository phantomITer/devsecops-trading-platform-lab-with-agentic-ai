from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    symbol = Column(String(20), nullable=False)          # 종목 코드
    quantity = Column(Float, default=0.0)
    avg_price = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))

    account = relationship("Account", back_populates="positions")