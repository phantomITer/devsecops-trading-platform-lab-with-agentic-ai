from sqlalchemy.orm import Session
from app.models.accounts import Account
from typing import Optional

def get_account(db: Session, agent_id: str) -> Optional[Account]:
    return db.query(Account).filter(Account.agent_id == agent_id).first()

def get_all_accounts(db: Session) -> list:
    return db.query(Account).all()

def create_account(db: Session, agent_id: str) -> Account:
    account = Account(agent_id=agent_id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def update_balance(db: Session, agent_id: str, delta: float) -> Optional[Account]:
    account = get_account(db, agent_id)
    if not account:
        return None
    account.balance += delta
    db.commit()
    db.refresh(account)
    return account

def init_all_accounts(db: Session):
    for agent_id in ["red", "blue", "institutional", "retail_a", "retail_b"]:
        if not get_account(db, agent_id):
            create_account(db, agent_id)