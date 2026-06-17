"""
agenticAi/core - Phase 2 Core Library

Public API exports for easy importing by agent modules.

Usage:
    from agenticAi.core import BaseAgent, MemoryStore, OllamaClient, RagEngine
    from agenticAi.core.tools import AlertTool, MarketDataTool, OrderTool, PortfolioTool
"""

from agenticAi.core.base import BaseAgent
from agenticAi.core.memory_store import MemoryStore
from agenticAi.core.llm.ollama_client import OllamaClient
from agenticAi.core.llm.rag_engine import RagEngine, Document

__all__ = [
    "BaseAgent",
    "MemoryStore",
    "OllamaClient",
    "RagEngine",
    "Document",
]
