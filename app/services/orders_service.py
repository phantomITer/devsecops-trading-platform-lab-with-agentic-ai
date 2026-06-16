# app/services/orders_service.py
from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.schemas.orders import Order, OrderCreate, OrderStatus, OrderType
from app.services import accounts_service

_fake_orders_db: List[Order] = []
_next_order_id: int = 1


def list_orders() -> List[Order]:
    return _fake_orders_db


def create_order(payload: OrderCreate) -> Order:
    global _next_order_id

    # 1) 계좌 존재 여부 확인
    account = accounts_service.get_account(payload.account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account {payload.account_id} does not exist",
        )

    # 2) 수량 검증 (양수)
    if payload.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0",
        )

    # 3) LIMIT 주문일 때 price 필수/양수 검증
    if payload.type == OrderType.LIMIT:
        if payload.price is None or payload.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit orders require a positive price",
            )

    # 4) MARKET 주문일 때는 price 무시 (None으로 통일)
    if payload.type == OrderType.MARKET:
        price = None
    else:
        price = payload.price

    order = Order(
        id=_next_order_id,
        account_id=payload.account_id,
        symbol=payload.symbol,
        side=payload.side,
        type=payload.type,
        quantity=payload.quantity,
        price=price,
        status=OrderStatus.NEW,
        created_at=datetime.utcnow(),
    )
    _fake_orders_db.append(order)
    _next_order_id += 1
    return order

def get_order(order_id: int):
    for order in _fake_orders_db:
        if order.id == order_id:
            return order
    return None