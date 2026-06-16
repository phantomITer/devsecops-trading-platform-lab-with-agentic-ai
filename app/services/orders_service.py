from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from app.schemas.orders import Order, OrderCreate, OrderStatus, OrderType
from app.database import SessionLocal
from app.models.orders import Order as OrderModel
from app.models.orders import OrderSide as ModelSide
from app.models.orders import OrderStatus as ModelStatus
from app.services import accounts_service


def _db():
    return SessionLocal()


def list_orders() -> List[Order]:
    db = _db()
    try:
        objs = db.query(OrderModel).all()
        return [_to_schema(obj) for obj in objs]
    finally:
        db.close()


def get_order(order_id: int) -> Optional[Order]:
    db = _db()
    try:
        obj = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not obj:
            return None
        return _to_schema(obj)
    finally:
        db.close()


def create_order(payload: OrderCreate) -> Order:
    # 1. 계좌 존재 확인
    account = accounts_service.get_account(payload.account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account {payload.account_id} does not exist",
        )

    # 2. 수량 검증
    if payload.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0",
        )

    # 3. LIMIT 주문 price 검증
    if payload.type == OrderType.LIMIT:
        if payload.price is None or payload.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit orders require a positive price",
            )

    price = None if payload.type == OrderType.MARKET else payload.price
    side  = ModelSide.LONG if payload.side.value == "BUY" else ModelSide.SHORT

    db = _db()
    try:
        obj = OrderModel(
            agent_id=str(payload.account_id),
            ticker=payload.symbol,
            side=side,
            quantity=int(payload.quantity),
            price=price,
            status=ModelStatus.PENDING,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return _to_schema(obj)
    finally:
        db.close()


def _to_schema(obj: OrderModel) -> Order:
    from app.schemas.orders import OrderSide, OrderType, OrderStatus
    side   = OrderSide.BUY  if obj.side == ModelSide.LONG  else OrderSide.SELL
    status = OrderStatus.NEW
    if obj.status == ModelStatus.FILLED:
        status = OrderStatus.FILLED
    elif obj.status == ModelStatus.CANCELLED:
        status = OrderStatus.CANCELED
    return Order(
        id=obj.id,
        account_id=int(obj.agent_id) if obj.agent_id.isdigit() else 0,
        symbol=obj.ticker,
        side=side,
        type=OrderType.MARKET,
        quantity=float(obj.quantity),
        price=obj.price,
        status=status,
        created_at=obj.created_at or datetime.utcnow(),
    )