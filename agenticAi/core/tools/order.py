from __future__ import annotations

from typing import Optional, Dict, Any
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class OrderTool:
    """
    Phase 2 - Agentic AI Core: tools/order.py
    Places and cancels orders on the trading platform via DB.

    Used by retail/institutional agents inside their act() method.
    All operations are logged via agent_logs when db is provided.
    """

    VALID_SIDES = {"buy", "sell"}
    VALID_ORDER_TYPES = {"market", "limit"}
    VALID_STATUSES = {"pending", "filled", "cancelled"}

    def __init__(self, db_session=None):
        self.db = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def place_order(
        self,
        account_id: int,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Place a new order.

        Args:
            account_id: The account placing the order.
            symbol: Ticker symbol (e.g. "AAPL").
            side: "buy" or "sell".
            order_type: "market" or "limit".
            quantity: Number of shares/units.
            price: Limit price (required for limit orders, None for market).

        Returns:
            Dict with 'success', 'order_id', and 'message'.
        """
        if side not in self.VALID_SIDES:
            return {"success": False, "message": f"Invalid side: {side}"}
        if order_type not in self.VALID_ORDER_TYPES:
            return {"success": False, "message": f"Invalid order_type: {order_type}"}
        if order_type == "limit" and price is None:
            return {"success": False, "message": "Limit order requires a price"}
        if self.db is None:
            return {"success": False, "message": "No DB session"}

        try:
            from app.models.order import Order
            order = Order(
                account_id=account_id,
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=Decimal(str(quantity)),
                price=Decimal(str(price)) if price is not None else None,
                status="pending",
            )
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            self.logger.info(
                "[OrderTool] Placed order id=%s %s %s %s qty=%s",
                order.id, side, order_type, symbol, quantity,
            )
            return {"success": True, "order_id": order.id, "message": "Order placed"}
        except Exception as exc:
            self.db.rollback()
            self.logger.error("[OrderTool] place_order error: %s", exc)
            return {"success": False, "message": str(exc)}

    def cancel_order(self, order_id: int) -> Dict[str, Any]:
        """
        Cancel a pending order by ID.
        Returns dict with 'success' and 'message'.
        """
        if self.db is None:
            return {"success": False, "message": "No DB session"}
        try:
            from app.models.order import Order
            order = self.db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return {"success": False, "message": f"Order {order_id} not found"}
            if order.status != "pending":
                return {"success": False, "message": f"Order {order_id} is {order.status}, cannot cancel"}
            order.status = "cancelled"
            self.db.commit()
            self.logger.info("[OrderTool] Cancelled order id=%s", order_id)
            return {"success": True, "order_id": order_id, "message": "Order cancelled"}
        except Exception as exc:
            self.db.rollback()
            self.logger.error("[OrderTool] cancel_order error: %s", exc)
            return {"success": False, "message": str(exc)}

    def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve an order by ID as a dict, or None if not found."""
        if self.db is None:
            return None
        try:
            from app.models.order import Order
            o = self.db.query(Order).filter(Order.id == order_id).first()
            if not o:
                return None
            return {
                "id": o.id,
                "account_id": o.account_id,
                "symbol": o.symbol,
                "side": o.side,
                "order_type": o.order_type,
                "quantity": float(o.quantity),
                "price": float(o.price) if o.price else None,
                "status": o.status,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
        except Exception as exc:
            self.logger.error("[OrderTool] get_order error: %s", exc)
            return None
