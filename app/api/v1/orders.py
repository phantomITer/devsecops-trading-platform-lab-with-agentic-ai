
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.orders_service import create_order, get_orders, get_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.post("/", response_model=OrderResponse, status_code=201)
def new_order(data: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, data)

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return get_order(db, order_id)
