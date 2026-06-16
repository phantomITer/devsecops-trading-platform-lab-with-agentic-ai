# fix_failures.py

# 1. schemas/accounts.py 수정
accounts_schema = '''from datetime import datetime
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
'''

# 2. services/accounts_service.py 수정
accounts_service = '''from datetime import datetime
from typing import List, Optional
from app.schemas.accounts import Account, AccountCreate
from app.database import SessionLocal
from app.models.accounts import Account as AccountModel


def _db():
    return SessionLocal()


def get_account(account_id: int) -> Optional[Account]:
    db = _db()
    try:
        obj = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if not obj:
            return None
        return Account(
            id=obj.id,
            name=obj.agent_id,
            currency="KRW",
            initial_balance=obj.equity or obj.balance,
            current_balance=obj.balance,
            created_at=obj.created_at or datetime.utcnow(),
        )
    finally:
        db.close()


def list_accounts() -> List[Account]:
    db = _db()
    try:
        objs = db.query(AccountModel).all()
        return [
            Account(
                id=obj.id,
                name=obj.agent_id,
                currency="KRW",
                initial_balance=obj.equity or obj.balance,
                current_balance=obj.balance,
                created_at=obj.created_at or datetime.utcnow(),
            )
            for obj in objs
        ]
    finally:
        db.close()


def create_account(payload: AccountCreate) -> Account:
    db = _db()
    try:
        obj = AccountModel(
            agent_id=payload.name,
            balance=payload.initial_balance,
            equity=payload.initial_balance,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return Account(
            id=obj.id,
            name=obj.agent_id,
            currency=payload.currency,
            initial_balance=payload.initial_balance,
            current_balance=obj.balance,
            created_at=obj.created_at or datetime.utcnow(),
        )
    finally:
        db.close()
'''

with open("app/schemas/accounts.py", "w", encoding="utf-8") as f:
    f.write(accounts_schema)
print("✅ app/schemas/accounts.py")

with open("app/services/accounts_service.py", "w", encoding="utf-8") as f:
    f.write(accounts_service)
print("✅ app/services/accounts_service.py")

print("\n--- 완료 ---")