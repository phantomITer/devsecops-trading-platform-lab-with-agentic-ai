from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # 문자열 컬럼들에 길이 지정
    name = Column(String(100), nullable=False)        # 계좌 이름, 100자 정도
    currency = Column(String(10), default="KRW")      # KRW, USD 등 3~5자, 10이면 충분

    initial_balance = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    owner = relationship("User", back_populates="accounts")
    orders = relationship("Order", back_populates="account")
    positions = relationship("Position", back_populates="account")