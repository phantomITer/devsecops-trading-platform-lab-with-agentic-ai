from __future__ import annotations

from typing import Any, Dict, List
import logging

from agenticAi.core.base import BaseAgent
from agenticAi.core.tools.market_data import MarketDataTool
from agenticAi.core.tools.order import OrderTool
from agenticAi.core.tools.portfolio import PortfolioTool


class InstitutionalAgent(BaseAgent):
    """
    Phase 2 - InstitutionalAgent (Large-volume Trading Agent)

    Simulates an institutional investor (e.g. fund/HFT) that:
      - perceive(): reads portfolio + market summaries for watched symbols.
      - decide(): applies a simple momentum strategy (buy if rising, sell if falling).
      - act(): places large block orders accordingly.

    Block orders are large quantity (BLOCK_SIZE) limit orders.
    """

    AGENT_TYPE = "institutional"
    BLOCK_SIZE = 1000  # shares per block order
    MOMENTUM_WINDOW = 10  # compare sell vs buy count

    def __init__(
        self,
        agent_id: str = "institutional-agent-1",
        db_session=None,
        ollama_client=None,
        memory_store=None,
        account_id: int = 1,
        watch_symbols: List[str] = None,
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type=self.AGENT_TYPE,
            db_session=db_session,
            ollama_client=ollama_client,
            memory_store=memory_store,
        )
        self.account_id = account_id
        self.watch_symbols = watch_symbols or ["AAPL", "TSLA", "MSFT"]
        self.market_tool = MarketDataTool(db_session=db_session)
        self.order_tool = OrderTool(db_session=db_session)
        self.portfolio_tool = PortfolioTool(db_session=db_session)

    # ------------------------------------------------------------------
    # BaseAgent interface
    # ------------------------------------------------------------------

    def perceive(self) -> Dict[str, Any]:
        """Gather market summaries for all watched symbols."""
        summaries = {
            symbol: self.market_tool.get_summary(symbol)
            for symbol in self.watch_symbols
        }
        portfolio = self.portfolio_tool.get_portfolio_summary(self.account_id)
        return {
            "account_id": self.account_id,
            "summaries": summaries,
            "portfolio": portfolio,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Momentum strategy:
        - If buy_count > sell_count -> bullish -> place BUY block order.
        - If sell_count > buy_count -> bearish -> place SELL block order.
        - Else -> hold.
        """
        orders_to_place = []
        for symbol, summary in perception["summaries"].items():
            buy_count = summary.get("buy_count", 0)
            sell_count = summary.get("sell_count", 0)
            if buy_count > sell_count:
                orders_to_place.append({"symbol": symbol, "side": "buy", "price": summary.get("latest_price")})
            elif sell_count > buy_count:
                orders_to_place.append({"symbol": symbol, "side": "sell", "price": summary.get("latest_price")})
        self.logger.info(
            "[InstitutionalAgent] decide: %d orders planned",
            len(orders_to_place),
        )
        return {
            "account_id": perception["account_id"],
            "orders_to_place": orders_to_place,
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Place block orders for each decision."""
        results = []
        for order in decision["orders_to_place"]:
            price = order.get("price")
            order_type = "limit" if price else "market"
            result = self.order_tool.place_order(
                account_id=decision["account_id"],
                symbol=order["symbol"],
                side=order["side"],
                order_type=order_type,
                quantity=self.BLOCK_SIZE,
                price=price,
            )
            results.append({"symbol": order["symbol"], "side": order["side"], "result": result})
            self.logger.info(
                "[InstitutionalAgent] act: %s %s -> %s",
                order["side"], order["symbol"], result.get("message"),
            )
        return {"orders_placed": results, "count": len(results)}
