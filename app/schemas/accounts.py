from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, example="Demo Account 1")
    currency: str = Field(..., example="USD")


class AccountCreate(AccountBase):
    initial_balance: float = Field(..., ge=0, example=10000.0)


class Account(AccountBase):
    id: int
    initial_balance: float
    current_balance: float
    created_at: datetime

    class Config:
        from_attributes = True
