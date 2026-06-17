
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.position import Position

def get_positions(db: Session):
    return db.query(Position).all()

def get_position(db: Session, position_id: int):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position
