from pydantic import BaseModel, Field
from typing import Optional

class InstrumentBase(BaseModel):
    symbol: str = Field(..., example="AAPL")
    name: str = Field(..., example="Apple Inc.")
    market: str = Field(..., example="US")  # KOSPI, KOSDAQ, US
    type: str = Field(..., example="STOCK")  # STOCK, ETF
    sector: Optional[str] = Field(None, example="Technology")
    currency: str = Field(..., example="USD")

class InstrumentOut(InstrumentBase):
    current_price: Optional[float] = Field(None, example=190.5)
    change_percent: Optional[float] = Field(None, example=1.2)  # %, +1.2 = 상승
    volume: Optional[int] = Field(None, example=1234567)