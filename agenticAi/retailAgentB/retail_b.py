from __future__ import annotations
from typing import Any, Dict
import logging
from agenticAi.core.base import BaseAgent
from agenticAi.core.tools.market_data import MarketDataTool
from agenticAi.core.tools.order import OrderTool
from agenticAi.core.tools.portfolio import PortfolioTool


class RetailAgentB(BaseAgent):
    """
    Phase 2 - RetailAgentB (Small Retail Investor - Momentum / FOMO Strategy)

    Strategy: "Chase the Trend"
    - perceive(): Get latest price, recent buy/sell counts, and current position.
    - decide(): If buy momentum is strong (buy_count significantly > sell_count),
      join the trend with a BUY order (FOMO / momentum chasing).
      If already holding and momentum reverses (sell pressure builds), SELL
      to cut losses (panic sell).
    - act(): Place the planned order.

    This agent represents a small retail investor driven by momentum and
    fear-of-missing-out (FOMO), the behavioral opposite of RetailAgentA.
    """

    AGENT_TYPE = "retail_b"
    ORDER_SIZE = 10          # Small retail order size
    MOMENTUM_THRESHOLD = 2   # buy_count must exceed sell_count by this factor
    LOSS_CUT_THRESHOLD = 0.03  # Panic sell if loss exceeds 3%

    def __init__(
        self,
        agent_id: str = "retail-agent-b-1",
        db_session=None,
        ollama_client=None,
        memory_store=None,
        account_id: int = 3,
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

        # Recall buy price from memory for loss-cut logic
        buy_price = self.recall("buy_price")

        return {
            "symbol": self.symbol,
            "summary": summary,
            "position": position,
            "buy_price": buy_price,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Momentum / FOMO logic:
        - BUY when buy_count > sell_count * MOMENTUM_THRESHOLD and not holding.
        - SELL (panic) when holding and price < buy_price * (1 - LOSS_CUT_THRESHOLD)
          or when sell pressure reverses the trend.
        """
        summary = perception["summary"]
        sell_count = summary.get("sell_count", 0)
        buy_count = summary.get("buy_count", 0)
        latest_price = summary.get("latest_price")
        position = perception["position"]
        buy_price = perception["buy_price"]

        # Panic sell / loss-cut logic
        if position and buy_price and latest_price:
            try:
                loss = (float(buy_price) - float(latest_price)) / float(buy_price)
                if loss >= self.LOSS_CUT_THRESHOLD:
                    return {
                        "action": "sell",
                        "reason": f"loss_cut loss={loss:.2%}",
                        "price": latest_price,
                    }
            except Exception:
                pass

            # Trend reversal panic: sell when sell pressure dominates while holding
            if sell_count > buy_count:
                return {
                    "action": "sell",
                    "reason": "trend_reversal_panic",
                    "price": latest_price,
                }

        # FOMO buy: join the uptrend when not holding
        if not position and buy_count > sell_count * self.MOMENTUM_THRESHOLD:
            return {
                "action": "buy",
                "reason": "momentum_fomo",
                "price": latest_price,
            }

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

        # Remember buy price for loss-cut tracking
        if side == "buy" and price:
            self.remember("buy_price", price)
        elif side == "sell":
            self.remember("buy_price", None)

        self.logger.info(
            "[RetailAgentB] act: %s %s -> %s",
            side, self.symbol, result.get("message"),
        )
        return {"action": action, "side": side, "order_result": result}
