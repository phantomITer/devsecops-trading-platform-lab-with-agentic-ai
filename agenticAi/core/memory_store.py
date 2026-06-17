from typing import Any, Dict, Optional
from threading import Lock
import logging

logger = logging.getLogger(__name__)


class MemoryStore:
    """
    Phase 2 - Agentic AI Core Library
    Thread-safe in-process key-value memory store for agent state.

    Each agent owns its own namespace (agent_id) inside the shared store.
    Values are stored in a nested dict: {agent_id: {key: value}}.

    Usage:
        store = MemoryStore()
        store.set("blue-agent-1", "last_scan_result", {"count": 3})
        store.get("blue-agent-1", "last_scan_result")
        store.clear_agent("blue-agent-1")
    """

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    def set(self, agent_id: str, key: str, value: Any) -> None:
        """Store a value under agent_id / key."""
        with self._lock:
            if agent_id not in self._store:
                self._store[agent_id] = {}
            self._store[agent_id][key] = value
            logger.debug("[MemoryStore] set agent=%s key=%s", agent_id, key)

    def get(self, agent_id: str, key: str, default: Any = None) -> Any:
        """Retrieve a value; returns default if not found."""
        with self._lock:
            return self._store.get(agent_id, {}).get(key, default)

    def delete(self, agent_id: str, key: str) -> None:
        """Delete a single key for an agent."""
        with self._lock:
            if agent_id in self._store and key in self._store[agent_id]:
                del self._store[agent_id][key]
                logger.debug("[MemoryStore] delete agent=%s key=%s", agent_id, key)

    def has(self, agent_id: str, key: str) -> bool:
        """Return True if agent_id/key exists."""
        with self._lock:
            return key in self._store.get(agent_id, {})

    # ------------------------------------------------------------------
    # Agent namespace helpers
    # ------------------------------------------------------------------

    def get_all(self, agent_id: str) -> Dict[str, Any]:
        """Return a copy of the entire memory namespace for an agent."""
        with self._lock:
            return dict(self._store.get(agent_id, {}))

    def clear_agent(self, agent_id: str) -> None:
        """Wipe all memory for a specific agent."""
        with self._lock:
            if agent_id in self._store:
                del self._store[agent_id]
                logger.info("[MemoryStore] cleared agent=%s", agent_id)

    def clear_all(self) -> None:
        """Wipe all memory for all agents. Use with caution."""
        with self._lock:
            self._store.clear()
            logger.warning("[MemoryStore] ALL agent memory cleared")

    def list_agents(self) -> list:
        """Return list of all agent_ids with stored data."""
        with self._lock:
            return list(self._store.keys())

    # ------------------------------------------------------------------
    # Singleton factory
    # ------------------------------------------------------------------

    _instance: Optional["MemoryStore"] = None

    @classmethod
    def get_instance(cls) -> "MemoryStore":
        """
        Return the process-wide singleton MemoryStore.
        Agents should use this unless a fresh store is needed for testing.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
