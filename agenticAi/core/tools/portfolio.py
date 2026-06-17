from __future__ import annotations

from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class PortfolioTool:
    """
    Phase 2 - Agentic AI Core: tools/portfolio.py
    Reads portfolio positions from the trading platform DB.

    Used by institutional/retail agents inside their perceive() method
    to assess current holdings before making trading decisions.
    """

    def __init__(self, db_session=None):
        self.db = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_positions(self, account_id: int) -> List[Dict[str, Any]]:
        """
        Return all open positions for an account as a list of dicts.
        Each dict has: symbol, quantity, avg_price, current_value.
        """
        if self.db is None:
            return []
        try:
            from app.models.position import Position
            rows = self.db.query(Position).filter(
                Position.account_id == account_id
            ).all()
            return [
                {
                    "id": r.id,
                    "account_id": r.account_id,
                    "symbol": r.symbol,
                    "quantity": float(r.quantity),
                    "avg_price": float(r.avg_price) if r.avg_price else None,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ]
        except Exception as exc:
            self.logger.error("[PortfolioTool] get_positions error: %s", exc)
            return []

    def get_position(self, account_id: int, symbol: str) -> Optional[Dict[str, Any]]:
        """Return a single position for account/symbol, or None."""
        if self.db is None:
            return None
        try:
            from app.models.position import Position
            row = (
                self.db.query(Position)
                .filter(Position.account_id == account_id, Position.symbol == symbol)
                .first()
            )
            if not row:
                return None
            return {
                "id": row.id,
                "account_id": row.account_id,
                "symbol": row.symbol,
                "quantity": float(row.quantity),
                "avg_price": float(row.avg_price) if row.avg_price else None,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
        except Exception as exc:
            self.logger.error("[PortfolioTool] get_position error: %s", exc)
            return None

    def get_portfolio_summary(self, account_id: int) -> Dict[str, Any]:
        """
        Summarize portfolio: total positions, total quantity, distinct symbols.
        """
        positions = self.get_positions(account_id)
        symbols = list({p["symbol"] for p in positions})
        total_qty = sum(p["quantity"] for p in positions)
        return {
            "account_id": account_id,
            "position_count": len(positions),
            "symbols": symbols,
            "total_quantity": total_qty,
        }

    def has_position(self, account_id: int, symbol: str) -> bool:
        """Return True if account holds a non-zero position in symbol."""
        pos = self.get_position(account_id, symbol)
        return pos is not None and pos.get("quantity", 0) != 0
