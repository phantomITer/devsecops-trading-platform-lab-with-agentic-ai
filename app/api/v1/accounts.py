
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.account import AccountCreate, AccountResponse
from app.services.accounts_service import create_account, get_accounts, get_account

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    return get_accounts(db)

@router.post("/", response_model=AccountResponse, status_code=201)
def new_account(data: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, data)

@router.get("/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    return get_account(db, account_id)
