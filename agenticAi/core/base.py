from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Any, Optional
import logging
import json

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Phase 2 - Agentic AI Core Library
    Base class for all trading platform agents.
    Provides common interface: run(), log_action(), perceive(), decide(), act()
    """

    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        db_session=None,
        ollama_client=None,
        memory_store=None,
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.db = db_session
        self.llm = ollama_client
        self.memory = memory_store
        self.is_running = False
        self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}[{self.agent_id}]"
        )

    # ------------------------------------------------------------------
    # Core agent lifecycle
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Main entry point. Orchestrates perceive -> decide -> act cycle.
        Returns a result dict that is also persisted to agent_logs.
        """
        self.is_running = True
        result = {}
        try:
            self.logger.info("[%s] run() started", self.agent_id)
            perception = self.perceive()
            decision = self.decide(perception)
            result = self.act(decision)
            self.log_action(action="run", result=result)
        except Exception as exc:
            self.logger.exception("[%s] run() error: %s", self.agent_id, exc)
            self.log_action(action="run_error", result={"error": str(exc)})
            result = {"error": str(exc)}
        finally:
            self.is_running = False
        return result

    @abstractmethod
    def perceive(self) -> dict:
        """
        Gather data from the environment (DB, market data, etc.).
        Must return a dict representing the agent's current observation.
        """
        ...

    @abstractmethod
    def decide(self, perception: dict) -> dict:
        """
        Process perception data and produce a decision dict.
        May use LLM, rule engine, or RAG.
        """
        ...

    @abstractmethod
    def act(self, decision: dict) -> dict:
        """
        Execute the decision (place order, emit alert, etc.).
        Returns a result dict describing what was done.
        """
        ...

    # ------------------------------------------------------------------
    # Logging / history persistence
    # ------------------------------------------------------------------

    def log_action(self, action: str, result: Any) -> None:
        """
        Persist an agent action log to the DB (agent_logs table).
        Falls back to console logging if DB session is not available.
        """
        result_str = result if isinstance(result, str) else json.dumps(result, default=str)
        if self.db is not None:
            try:
                from app.models.agent_log import AgentLog
                entry = AgentLog(
                    agent_id=self.agent_id,
                    agent_type=self.agent_type,
                    action=action,
                    result=result_str,
                )
                self.db.add(entry)
                self.db.commit()
                self.logger.debug("[%s] log_action persisted: %s", self.agent_id, action)
            except Exception as exc:
                self.logger.error("[%s] log_action DB error: %s", self.agent_id, exc)
                self.db.rollback()
        else:
            self.logger.info("[%s] action=%s result=%s", self.agent_id, action, result_str)

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def ask_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a prompt to the configured Ollama LLM client.
        Returns empty string if no LLM is configured.
        """
        if self.llm is None:
            self.logger.warning("[%s] No LLM client configured", self.agent_id)
            return ""
        return self.llm.chat(prompt=prompt, system_prompt=system_prompt)

    def recall(self, key: str) -> Any:
        """Retrieve a value from the agent's memory store."""
        if self.memory is None:
            return None
        return self.memory.get(self.agent_id, key)

    def remember(self, key: str, value: Any) -> None:
        """Persist a value in the agent's memory store."""
        if self.memory is None:
            return
        self.memory.set(self.agent_id, key, value)

    def status(self) -> dict:
        """Return a summary of the agent's current state."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "is_running": self.is_running,
            "timestamp": datetime.now(UTC).isoformat(),
        }
