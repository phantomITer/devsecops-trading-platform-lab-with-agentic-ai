from __future__ import annotations

from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class MarketDataTool:
    """
    Phase 2 - Agentic AI Core: tools/market_data.py
    Retrieves market price and order-book data from the trading platform DB.

    Agents use this tool inside their perceive() method to get current
    market state without querying the DB directly.
    """

    def __init__(self, db_session=None):
        self.db = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Ticker / Price
    # ------------------------------------------------------------------

    def get_price(self, symbol: str) -> Optional[float]:
        """
        Return the latest price for a symbol.
        Queries the most recent filled order price as a proxy.
        Returns None if no data is available.
        """
        if self.db is None:
            self.logger.warning("[MarketDataTool] No DB session")
            return None
        try:
            from app.models.order import Order
            from sqlalchemy import desc
            row = (
                self.db.query(Order)
                .filter(Order.symbol == symbol, Order.status == "filled")
                .order_by(desc(Order.created_at))
                .first()
            )
            return float(row.price) if row and row.price else None
        except Exception as exc:
            self.logger.error("[MarketDataTool] get_price error: %s", exc)
            return None

    def get_recent_orders(
        self,
        symbol: str,
        limit: int = 20,
        side: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return recent orders for a symbol as a list of dicts.
        Optionally filter by side ("buy" | "sell").
        """
        if self.db is None:
            return []
        try:
            from app.models.order import Order
            from sqlalchemy import desc
            q = self.db.query(Order).filter(Order.symbol == symbol)
            if side:
                q = q.filter(Order.side == side)
            rows = q.order_by(desc(Order.created_at)).limit(limit).all()
            return [
                {
                    "id": r.id,
                    "symbol": r.symbol,
                    "side": r.side,
                    "order_type": r.order_type,
                    "quantity": float(r.quantity),
                    "price": float(r.price) if r.price else None,
                    "status": r.status,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ]
        except Exception as exc:
            self.logger.error("[MarketDataTool] get_recent_orders error: %s", exc)
            return []

    def get_symbols(self) -> List[str]:
        """Return all distinct symbols that have orders."""
        if self.db is None:
            return []
        try:
            from app.models.order import Order
            rows = self.db.query(Order.symbol).distinct().all()
            return [r.symbol for r in rows]
        except Exception as exc:
            self.logger.error("[MarketDataTool] get_symbols error: %s", exc)
            return []

    def get_summary(self, symbol: str) -> Dict[str, Any]:
        """
        Return a brief market summary dict for a symbol:
        latest_price, buy_count, sell_count, total_volume.
        """
        summary: Dict[str, Any] = {
            "symbol": symbol,
            "latest_price": self.get_price(symbol),
            "buy_count": 0,
            "sell_count": 0,
            "total_volume": 0.0,
        }
        if self.db is None:
            return summary
        try:
            from app.models.order import Order
            orders = self.db.query(Order).filter(Order.symbol == symbol).all()
            for o in orders:
                if o.side == "buy":
                    summary["buy_count"] += 1
                elif o.side == "sell":
                    summary["sell_count"] += 1
                if o.quantity:
                    summary["total_volume"] += float(o.quantity)
        except Exception as exc:
            self.logger.error("[MarketDataTool] get_summary error: %s", exc)
        return summary
