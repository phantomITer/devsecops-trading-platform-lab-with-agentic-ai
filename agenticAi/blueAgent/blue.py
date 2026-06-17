from __future__ import annotations

from typing import Any, Dict, Optional
import logging

from agenticAi.core.base import BaseAgent
from agenticAi.core.tools.alert import AlertTool
from agenticAi.core.tools.market_data import MarketDataTool


class BlueAgent(BaseAgent):
    """
    Phase 2 - BlueAgent (Defensive Security Agent)

    Responsibilities:
      - perceive(): Scan recent security events and order anomalies.
      - decide(): Use KISA RAG + LLM to assess threat level and recommend response.
      - act(): Emit security alerts for detected threats.

    This agent implements the defensive (blue team) role in the
    DevSecOps trading platform simulation.
    """

    AGENT_TYPE = "blue"
    ANOMALY_THRESHOLD = 5  # >5 sell orders in a short window = suspicious

    def __init__(
        self,
        agent_id: str = "blue-agent-1",
        db_session=None,
        ollama_client=None,
        memory_store=None,
        rag_engine=None,
        watch_symbol: str = "AAPL",
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type=self.AGENT_TYPE,
            db_session=db_session,
            ollama_client=ollama_client,
            memory_store=memory_store,
        )
        self.rag = rag_engine
        self.watch_symbol = watch_symbol
        self.alert_tool = AlertTool(db_session=db_session)
        self.market_tool = MarketDataTool(db_session=db_session)

    # ------------------------------------------------------------------
    # BaseAgent interface implementation
    # ------------------------------------------------------------------

    def perceive(self) -> Dict[str, Any]:
        """
        Gather market data and recent security events.
        Returns a perception dict used by decide().
        """
        recent_orders = self.market_tool.get_recent_orders(
            self.watch_symbol, limit=50
        )
        recent_alerts = self.alert_tool.get_recent_alerts(limit=10)
        sell_orders = [o for o in recent_orders if o.get("side") == "sell"]
        perception = {
            "symbol": self.watch_symbol,
            "total_recent_orders": len(recent_orders),
            "sell_order_count": len(sell_orders),
            "recent_alerts": recent_alerts,
            "latest_price": self.market_tool.get_price(self.watch_symbol),
        }
        self.logger.debug(
            "[BlueAgent] perceive: %d orders (%d sells)",
            len(recent_orders), len(sell_orders),
        )
        return perception

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess threat based on sell order volume.
        Optionally use RAG/LLM to enrich the recommendation.
        Returns a decision dict.
        """
        sell_count = perception.get("sell_order_count", 0)
        threat_detected = sell_count >= self.ANOMALY_THRESHOLD

        decision: Dict[str, Any] = {
            "threat_detected": threat_detected,
            "sell_count": sell_count,
            "symbol": perception.get("symbol"),
            "severity": "high" if sell_count >= self.ANOMALY_THRESHOLD * 2 else "medium" if threat_detected else "low",
            "llm_analysis": "",
        }

        if threat_detected and self.rag is not None:
            question = (
                f"{sell_count} sell orders detected for {perception.get('symbol')} "
                "in a short window. Is this insider trading or coordinated dump? "
                "Recommend defensive action per KISA guidelines."
            )
            decision["llm_analysis"] = self.rag.query(question)
        elif threat_detected and self.llm is not None:
            prompt = (
                f"Security alert: {sell_count} sell orders for {perception.get('symbol')}. "
                "Assess threat and recommend action."
            )
            decision["llm_analysis"] = self.ask_llm(prompt)

        self.logger.info(
            "[BlueAgent] decide: threat=%s severity=%s",
            threat_detected, decision["severity"],
        )
        return decision

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        If threat detected, create a security alert in the DB.
        Returns result dict.
        """
        if not decision.get("threat_detected"):
            return {
                "action": "no_action",
                "reason": f"sell_count={decision.get('sell_count')} below threshold",
            }

        description = (
            f"Anomalous sell activity detected: {decision['sell_count']} sell orders "
            f"for {decision['symbol']}. Severity: {decision['severity']}. "
            f"LLM: {decision.get('llm_analysis', '')[:200]}"
        )
        alert_result = self.alert_tool.create_alert(
            event_type="anomaly",
            severity=decision["severity"],
            source=self.agent_id,
            description=description,
        )
        self.logger.info(
            "[BlueAgent] act: alert created=%s",
            alert_result.get("event_id"),
        )
        return {
            "action": "alert_created",
            "alert_result": alert_result,
            "decision": decision,
        }
