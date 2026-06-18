
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class AccountCreate(BaseModel):
    name: str = Field(..., max_length=100)
    currency: str                    # 필수 - 누락 시 422
    initial_balance: float = 0.0    # 0은 합리적 기본값이므로 유지

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("name must not be empty")
        return v

    @field_validator("initial_balance")
    @classmethod
    def balance_non_negative(cls, v):
        if v < 0:
            raise ValueError("initial_balance must be >= 0")
        return v

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    currency: str
    initial_balance: float
    current_balance: float
    created_at: datetime
