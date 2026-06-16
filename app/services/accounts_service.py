# app/services/accounts_service.py
from datetime import datetime
from typing import List, Optional

from app.schemas.accounts import Account, AccountCreate

_fake_db: List[Account] = []
_next_id: int = 1


def get_account(account_id: int) -> Optional[Account]:
    for acc in _fake_db:
        if acc.id == account_id:
            return acc
    return None


def list_accounts() -> List[Account]:
    return _fake_db


def create_account(payload: AccountCreate) -> Account:
    global _next_id

    account = Account(
        id=_next_id,
        name=payload.name,
        currency=payload.currency,
        initial_balance=payload.initial_balance,
        current_balance=payload.initial_balance,
        created_at=datetime.utcnow(),
    )
    _fake_db.append(account)
    _next_id += 1
    return account