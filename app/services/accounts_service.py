
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.account import Account
from app.schemas.account import AccountCreate

def create_account(db: Session, data: AccountCreate) -> Account:
    account = Account(
        name=data.name,
        currency=data.currency,
        initial_balance=data.initial_balance,
        current_balance=data.initial_balance,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_accounts(db: Session):
    return db.query(Account).all()

def get_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
