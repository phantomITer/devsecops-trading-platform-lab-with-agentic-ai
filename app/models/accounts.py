from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"
    id             = Column(Integer, primary_key=True, index=True)
    agent_id       = Column(String, unique=True, index=True, nullable=False)
    balance        = Column(Float, default=10_000_000.0)
    equity         = Column(Float, default=10_000_000.0)
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl   = Column(Float, default=0.0)
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime, server_default=func.now())
    updated_at     = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Account agent={self.agent_id} balance={self.balance}>"