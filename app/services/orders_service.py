from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order import Order
from app.models.account import Account
from app.models.position import Position
from app.schemas.order import OrderCreate


def _execute_order_and_update_state(db: Session, order: Order) -> None:
    """
    주문을 즉시 체결(FILLED)로 가정하고,
    - Account.current_balance
    - Position
    을 업데이트한다.
    BUY / SELL 모두 처리.
    """
    # 1) 계좌 조회
    account = db.query(Account).filter(Account.id == order.account_id).first()
    if not account:
        raise HTTPException(status_code=400, detail=f"Account {order.account_id} does not exist")

    # 가격/수량 필수
    if order.price is None or order.quantity is None:
        raise HTTPException(status_code=400, detail="Order must have price and quantity to be executed")

    cost = order.price * order.quantity

    # 2) 계좌 잔고 초기화
    if account.current_balance is None:
        account.current_balance = account.initial_balance or 0.0

    # 3) BUY / SELL 에 따라 계좌 잔고 변경
    if order.side == "BUY":
        # 잔고 부족 체크 (공매수 금지)
        if account.current_balance < cost:
            raise HTTPException(status_code=400, detail="Insufficient balance for BUY order")

        account.current_balance -= cost

    elif order.side == "SELL":
        account.current_balance += cost

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported order side: {order.side}")

    # 4) 포지션 조회
    position = (
        db.query(Position)
        .filter(
            Position.account_id == order.account_id,
            Position.symbol == order.symbol,
        )
        .first()
    )

    if order.side == "BUY":
        # BUY: 포지션 생성 또는 평단/수량 증가
        if position is None:
            position = Position(
                account_id=order.account_id,
                symbol=order.symbol,
                quantity=order.quantity,
                avg_price=order.price,
            )
            db.add(position)
        else:
            old_qty = position.quantity or 0.0
            old_avg = position.avg_price or 0.0
            new_qty = old_qty + order.quantity

            if new_qty <= 0:
                position.quantity = 0.0
                position.avg_price = 0.0
            else:
                position.avg_price = (old_qty * old_avg + order.quantity * order.price) / new_qty
                position.quantity = new_qty

    elif order.side == "SELL":
        # SELL: 포지션 없으면 에러
        if position is None:
            raise HTTPException(status_code=400, detail="Cannot sell: no existing position")

        old_qty = position.quantity or 0.0
        new_qty = old_qty - order.quantity

        # 보유 수량보다 많이 팔면 에러 (공매도 금지)
        if new_qty < 0:
            raise HTTPException(status_code=400, detail="Cannot sell more than current position quantity")

        position.quantity = new_qty

        # 전량 매도 시 평단 리셋
        if new_qty == 0:
            position.avg_price = 0.0
        # new_qty > 0 이면 avg_price 유지

    # 5) 주문 상태를 FILLED 로 변경
    order.status = "FILLED"


def create_order(db: Session, data: OrderCreate) -> Order:
    """
    주문 생성 + 즉시 체결 (시뮬레이션용).
    """
    # 0) 계좌 존재 여부 검증
    account = db.query(Account).filter(Account.id == data.account_id).first()
    if not account:
        raise HTTPException(status_code=400, detail=f"Account {data.account_id} does not exist")

    # 0-1) LIMIT 주문 검증
    if data.order_type == "LIMIT" and (data.price is None or data.price <= 0):
        raise HTTPException(status_code=400, detail="Limit orders require a positive price")

    # 1) 주문 생성 (status=NEW)
    order = Order(
        account_id=data.account_id,
        symbol=data.symbol,
        side=data.side,
        order_type=data.order_type,
        quantity=data.quantity,
        price=data.price,
        status="NEW",
    )
    db.add(order)
    db.flush()  # order.id 확보

    # 2) 주문 체결 + 포지션/잔고 업데이트
    _execute_order_and_update_state(db, order)

    # 3) 커밋 및 리프레시
    db.commit()
    db.refresh(order)

    return order


def get_orders(db: Session):
    return db.query(Order).all()


def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order