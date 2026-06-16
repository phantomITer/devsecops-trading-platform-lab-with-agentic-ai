from datetime import datetime
from typing import List, Optional
from app.schemas.accounts import Account, AccountCreate
from app.database import SessionLocal
from app.models.accounts import Account as AccountModel
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


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
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Account name already exists")
    finally:
        db.close()


def init_all_accounts(db):
    agent_ids = ["red", "blue", "institutional", "retail_a", "retail_b"]
    for agent_id in agent_ids:
        exists = db.query(AccountModel).filter(
            AccountModel.agent_id == agent_id
        ).first()
        if not exists:
            obj = AccountModel(
                agent_id=agent_id,
                balance=10_000_000.0,
                equity=10_000_000.0,
            )
            db.add(obj)
    db.commit()
