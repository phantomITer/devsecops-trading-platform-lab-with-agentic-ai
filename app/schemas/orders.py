from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(str, Enum):
    NEW = "NEW"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELED = "CANCELED"


class OrderBase(BaseModel):
    account_id: int = Field(..., example=1)
    symbol: str = Field(..., example="AAPL")
    side: OrderSide = Field(..., example=OrderSide.BUY)
    type: OrderType = Field(..., example=OrderType.LIMIT)
    quantity: float = Field(..., gt=0, example=10)
    price: float | None = Field(
        None,
        example=190.5,
        description="Limit 주문에서만 필요한 가격",
    )


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True