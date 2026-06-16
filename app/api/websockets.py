# app/api/orders.py
from typing import List

from fastapi import APIRouter, status, HTTPException

from app.schemas.orders import Order, OrderCreate
from app.services import orders_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[Order])
def get_orders():
    return orders_service.list_orders()


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate):
    return orders_service.create_order(payload)


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = orders_service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order