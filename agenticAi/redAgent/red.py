from __future__ import annotations

from typing import Any, Dict
import random
import logging

from agenticAi.core.base import BaseAgent
from agenticAi.core.tools.alert import AlertTool
from agenticAi.core.tools.order import OrderTool
from agenticAi.core.tools.market_data import MarketDataTool


class RedAgent(BaseAgent):
    """
    Phase 2 - RedAgent (Offensive / Attack Simulation Agent)

    Responsibilities:
      - perceive(): Observe available symbols and current market state.
      - decide(): Choose an attack scenario to simulate (e.g. spoofing,
                  coordinated dump, insider trade).
      - act(): Execute the simulated attack as orders + emit a simulation
               security event so the BlueAgent can detect it.

    This is a RED TEAM simulation agent - it does NOT cause real harm.
    All actions are tagged as 'simulation' in security_events.
    """

    AGENT_TYPE = "red"

    ATTACK_SCENARIOS = [
        "coordinated_dump",
        "spoofing",
        "wash_trading",
        "front_running",
    ]

    def __init__(
        self,
        agent_id: str = "red-agent-1",
        db_session=None,
        ollama_client=None,
        memory_store=None,
        target_account_id: int = 1,
        target_symbol: str = "AAPL",
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type=self.AGENT_TYPE,
            db_session=db_session,
            ollama_client=ollama_client,
            memory_store=memory_store,
        )
        self.target_account_id = target_account_id
        self.target_symbol = target_symbol
        self.alert_tool = AlertTool(db_session=db_session)
        self.order_tool = OrderTool(db_session=db_session)
        self.market_tool = MarketDataTool(db_session=db_session)

    # ------------------------------------------------------------------
    # BaseAgent interface
    # ------------------------------------------------------------------

    def perceive(self) -> Dict[str, Any]:
        """Observe current market state for the target symbol."""
        summary = self.market_tool.get_summary(self.target_symbol)
        return {
            "symbol": self.target_symbol,
            "market_summary": summary,
            "available_scenarios": self.ATTACK_SCENARIOS,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Choose an attack scenario randomly (simulation purposes)."""
        scenario = random.choice(self.ATTACK_SCENARIOS)
        self.logger.info("[RedAgent] decide: selected scenario=%s", scenario)
        return {
            "scenario": scenario,
            "symbol": perception["symbol"],
            "account_id": self.target_account_id,
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate the chosen attack:
        - Place a burst of orders to mimic the scenario.
        - Log a 'simulation' security event.
        """
        scenario = decision["scenario"]
        symbol = decision["symbol"]
        account_id = decision["account_id"]
        placed_orders = []

        if scenario == "coordinated_dump":
            for _ in range(6):
                result = self.order_tool.place_order(
                    account_id=account_id, symbol=symbol,
                    side="sell", order_type="market", quantity=100,
                )
                placed_orders.append(result)

        elif scenario == "spoofing":
            for _ in range(4):
                result = self.order_tool.place_order(
                    account_id=account_id, symbol=symbol,
                    side="buy", order_type="limit", quantity=500,
                    price=round(random.uniform(100, 200), 2),
                )
                placed_orders.append(result)

        elif scenario == "wash_trading":
            for _ in range(3):
                self.order_tool.place_order(
                    account_id=account_id, symbol=symbol,
                    side="buy", order_type="market", quantity=50,
                )
                result = self.order_tool.place_order(
                    account_id=account_id, symbol=symbol,
                    side="sell", order_type="market", quantity=50,
                )
                placed_orders.append(result)

        elif scenario == "front_running":
            result = self.order_tool.place_order(
                account_id=account_id, symbol=symbol,
                side="buy", order_type="market", quantity=1000,
            )
            placed_orders.append(result)

        # Log simulation event
        alert_result = self.alert_tool.create_alert(
            event_type="simulation",
            severity="high",
            source=self.agent_id,
            description=f"Red team simulation: {scenario} on {symbol}",
        )

        self.logger.info(
            "[RedAgent] act: scenario=%s orders=%d alert=%s",
            scenario, len(placed_orders), alert_result.get("event_id"),
        )
        return {
            "scenario": scenario,
            "placed_orders": placed_orders,
            "alert_result": alert_result,
        }
