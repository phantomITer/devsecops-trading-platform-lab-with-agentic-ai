# app/api/accounts.py

from typing import List
from fastapi import APIRouter, status, HTTPException
from app.schemas.accounts import Account, AccountCreate
from app.services import accounts_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


# trailing slash 제거
@router.get("", response_model=List[Account])   # "/" → ""
def get_accounts():
    return accounts_service.list_accounts()

@router.post("", response_model=Account, status_code=status.HTTP_201_CREATED)  # "/" → ""
def create_account(payload: AccountCreate):
    return accounts_service.create_account(payload)

@router.get("/{account_id}", response_model=Account)
def get_account(account_id: int):
    account = accounts_service.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account