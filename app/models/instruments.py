from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.sql import func
from app.database import Base

class Instrument(Base):
    __tablename__ = "instruments"
    id          = Column(Integer, primary_key=True, index=True)
    ticker      = Column(String, unique=True, index=True, nullable=False)
    name        = Column(String, nullable=False)
    market      = Column(String, default="KOSPI")
    open_price  = Column(Float, nullable=True)
    high_price  = Column(Float, nullable=True)
    low_price   = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    volume      = Column(BigInteger, nullable=True)
    updated_at  = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Instrument {self.ticker} {self.name}>"