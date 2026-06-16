# app/schemas/accounts.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    name: str = Field(..., example="Demo Account 1")
    currency: str = Field(..., example="USD")


class AccountCreate(AccountBase):
    initial_balance: float = Field(..., ge=0, example=10000.0)


class Account(AccountBase):
    id: int
    initial_balance: float
    current_balance: float
    created_at: datetime

    class Config:
        from_attributes = True  # 나중에 ORM 모델과 연동할 때 유용