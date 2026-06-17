
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.security_event import SecurityEventCreate, SecurityEventResponse
from app.services.security_event_service import create_security_event, get_security_events

router = APIRouter(prefix="/security-events", tags=["security-events"])

@router.get("/", response_model=List[SecurityEventResponse])
def list_events(db: Session = Depends(get_db)):
    return get_security_events(db)

@router.post("/", response_model=SecurityEventResponse, status_code=201)
def new_event(data: SecurityEventCreate, db: Session = Depends(get_db)):
    return create_security_event(db, data)
