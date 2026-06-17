
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.position import PositionResponse
from app.services.positions_service import get_positions, get_position

router = APIRouter(prefix="/positions", tags=["positions"])

@router.get("/", response_model=List[PositionResponse])
def list_positions(db: Session = Depends(get_db)):
    return get_positions(db)

@router.get("/{position_id}", response_model=PositionResponse)
def read_position(position_id: int, db: Session = Depends(get_db)):
    return get_position(db, position_id)
