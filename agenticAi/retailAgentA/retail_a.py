from __future__ import annotations

from typing import Any, Dict
import logging

from agenticAi.core.base import BaseAgent
from agenticAi.core.tools.market_data import MarketDataTool
from agenticAi.core.tools.order import OrderTool
from agenticAi.core.tools.portfolio import PortfolioTool


class RetailAgentA(BaseAgent):
    """
    Phase 2 - RetailAgentA (Small Retail Investor - Value Strategy)

    Strategy: "Buy the Dip"
      - perceive(): Get latest price and recent order count.
      - decide(): If sell pressure is high (price potentially dipping),
                  plan a small BUY order (contrarian value approach).
                  If already holding, consider taking profit (SELL).
      - act(): Place the planned order.

    This agent represents a small retail investor with a value-oriented,
    contrarian strategy.
    """

    AGENT_TYPE = "retail_a"
    ORDER_SIZE = 10  # Small retail order size
    PROFIT_THRESHOLD = 0.05  # Take profit at 5% gain

    def __init__(
        self,
        agent_id: str = "retail-agent-a-1",
        db_session=None,
        ollama_client=None,
        memory_store=None,
        account_id: int = 2,
        symbol: str = "AAPL",
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type=self.AGENT_TYPE,
            db_session=db_session,
            ollama_client=ollama_client,
            memory_store=memory_store,
        )
        self.account_id = account_id
        self.symbol = symbol
        self.market_tool = MarketDataTool(db_session=db_session)
        self.order_tool = OrderTool(db_session=db_session)
        self.portfolio_tool = PortfolioTool(db_session=db_session)

    # ------------------------------------------------------------------
    # BaseAgent interface
    # ------------------------------------------------------------------

    def perceive(self) -> Dict[str, Any]:
        """Read market summary and current position."""
        summary = self.market_tool.get_summary(self.symbol)
        position = self.portfolio_tool.get_position(self.account_id, self.symbol)
        # Recall buy price from memory
        buy_price = self.recall("buy_price")
        return {
            "symbol": self.symbol,
            "summary": summary,
            "position": position,
            "buy_price": buy_price,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Buy the dip: if sell pressure > buy pressure, plan to buy.
        Take profit: if holding and price > buy_price * (1 + threshold).
        """
        summary = perception["summary"]
        sell_count = summary.get("sell_count", 0)
        buy_count = summary.get("buy_count", 0)
        latest_price = summary.get("latest_price")
        position = perception["position"]
        buy_price = perception["buy_price"]

        # Take profit logic
        if position and buy_price and latest_price:
            try:
                gain = (float(latest_price) - float(buy_price)) / float(buy_price)
                if gain >= self.PROFIT_THRESHOLD:
                    return {"action": "sell", "reason": f"take_profit gain={gain:.2%}", "price": latest_price}
            except Exception:
                pass

        # Buy the dip
        if sell_count > buy_count and not position:
            return {"action": "buy", "reason": "sell_pressure_dip", "price": latest_price}

        return {"action": "hold", "reason": "no_signal"}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute buy/sell or hold."""
        action = decision.get("action")
        if action == "hold":
            return {"action": "hold", "reason": decision.get("reason")}

        side = "buy" if action == "buy" else "sell"
        price = decision.get("price")
        order_type = "limit" if price else "market"
        result = self.order_tool.place_order(
            account_id=self.account_id,
            symbol=self.symbol,
            side=side,
            order_type=order_type,
            quantity=self.ORDER_SIZE,
            price=price,
        )

        # Remember buy price for profit tracking
        if side == "buy" and price:
            self.remember("buy_price", price)
        elif side == "sell":
            self.remember("buy_price", None)

        self.logger.info(
            "[RetailAgentA] act: %s %s -> %s",
            side, self.symbol, result.get("message"),
        )
        return {"action": action, "side": side, "order_result": result}
