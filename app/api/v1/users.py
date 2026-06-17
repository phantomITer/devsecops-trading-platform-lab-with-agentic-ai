
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserResponse
from app.services.user_service import get_users, get_user, delete_user
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_user(db, user_id)

@router.delete("/{user_id}", status_code=204)
def remove_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    delete_user(db, user_id)
