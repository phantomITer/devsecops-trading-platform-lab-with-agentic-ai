"""Phase 2 - Agentic AI Core Library Tests

Tests for the BaseAgent abstract class and all agent implementations:
- BlueAgent (defensive security)
- RedAgent (offensive security simulation)
- InstitutionalAgent (momentum block trading)
- RetailAgentA (buy-the-dip value strategy)
- RetailAgentB (momentum FOMO strategy)

All agents inherit from BaseAgent and implement:
- perceive(): data gathering
- decide(): decision-making with LLM/RAG support
- act(): action execution
- log_action(): history persistence
"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import Mock, MagicMock, patch
import json

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from agenticAi.core.base import BaseAgent
from agenticAi.core.memory_store import MemoryStore
from agenticAi.core.llm.ollama_client import OllamaClient
from agenticAi.blueAgent.blue import BlueAgent
from agenticAi.redAgent.red import RedAgent
from agenticAi.institutionalAgent.institutional import InstitutionalAgent
from agenticAi.retailAgentA.retail_a import RetailAgentA
from agenticAi.retailAgentB.retail_b import RetailAgentB


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------
@pytest.fixture
def mock_db_session():
    """Mock database session for testing without DB dependency."""
    db_mock = Mock()
    db_mock.add = Mock()
    db_mock.commit = Mock()
    db_mock.rollback = Mock()
    return db_mock


@pytest.fixture
def memory_store():
    """Shared in-process memory store."""
    return MemoryStore()


@pytest.fixture
def mock_ollama_client():
    """Mock OllamaClient for testing LLM interactions."""
    ollama_mock = Mock(spec=OllamaClient)
    ollama_mock.chat = Mock(return_value="LLM response: all clear")
    return ollama_mock


# ------------------------------------------------------------------
# Test BaseAgent abstract interface
# ------------------------------------------------------------------
def test_base_agent_cannot_instantiate():
    """BaseAgent is abstract and should not be instantiated directly."""
    with pytest.raises(TypeError):
        BaseAgent(agent_id="test", agent_type="test")


class ConcreteTestAgent(BaseAgent):
    """Minimal concrete implementation for testing BaseAgent interface."""

    def perceive(self):
        return {"data": "test perception"}

    def decide(self, perception):
        return {"decision": "test decision"}

    def act(self, decision):
        return {"action": "test action"}


def test_concrete_agent_lifecycle(mock_db_session, memory_store, mock_ollama_client):
    """Test that concrete agent implements full lifecycle: run() -> perceive -> decide -> act."""
    agent = ConcreteTestAgent(
        agent_id="test-1",
        agent_type="test",
        db_session=mock_db_session,
        ollama_client=mock_ollama_client,
        memory_store=memory_store,
    )

    result = agent.run()

    assert result["action"] == "test action"
    assert agent.is_running == False
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


def test_base_agent_memory_operations(memory_store):
    """Test BaseAgent remember() and recall() methods."""
    agent = ConcreteTestAgent(
        agent_id="mem-test", agent_type="test", memory_store=memory_store
    )

    agent.remember("key1", "value1")
    agent.remember("counter", 42)

    assert agent.recall("key1") == "value1"
    assert agent.recall("counter") == 42
    assert agent.recall("missing") is None


def test_base_agent_llm_integration(mock_ollama_client, memory_store):
    """Test BaseAgent ask_llm() helper."""
    agent = ConcreteTestAgent(
        agent_id="llm-test",
        agent_type="test",
        ollama_client=mock_ollama_client,
        memory_store=memory_store,
    )

    response = agent.ask_llm("test prompt", system_prompt="system")

    assert response == "LLM response: all clear"
    mock_ollama_client.chat.assert_called_once_with(
        prompt="test prompt", system_prompt="system"
    )


def test_base_agent_status():
    """Test agent.status() returns correct metadata."""
    agent = ConcreteTestAgent(agent_id="status-test", agent_type="test")
    status = agent.status()

    assert status["agent_id"] == "status-test"
    assert status["agent_type"] == "test"
    assert status["is_running"] == False
    assert "timestamp" in status


# ------------------------------------------------------------------
# Test BlueAgent (Defensive Security)
# ------------------------------------------------------------------
def test_blue_agent_initialization(mock_db_session, memory_store):
    """Test BlueAgent initializes with correct defaults."""
    agent = BlueAgent(
        db_session=mock_db_session,
        memory_store=memory_store,
        watch_symbol="AAPL",
    )

    assert agent.agent_id == "blue-agent-1"
    assert agent.agent_type == "blue"
    assert agent.watch_symbol == "AAPL"


@patch("agenticAi.blueAgent.blue.MarketDataTool")
@patch("agenticAi.blueAgent.blue.AlertTool")
def test_blue_agent_perceive(mock_alert_tool, mock_market_tool, mock_db_session, memory_store):
    """Test BlueAgent.perceive() scans for security anomalies."""
    mock_market_instance = Mock()
    mock_market_instance.get_recent_orders = Mock(return_value=[])
    mock_market_tool.return_value = mock_market_instance

    agent = BlueAgent(db_session=mock_db_session, memory_store=memory_store)
    perception = agent.perceive()

    assert "recent_orders" in perception
    assert "order_count" in perception
    mock_market_instance.get_recent_orders.assert_called_once()


def test_blue_agent_run_basic(mock_db_session, memory_store):
    """Test BlueAgent full run() cycle without mocking internals."""
    agent = BlueAgent(db_session=mock_db_session, memory_store=memory_store)

    result = agent.run()

    assert "status" in result
    assert agent.is_running == False


# ------------------------------------------------------------------
# Test RedAgent (Offensive Security Simulation)
# ------------------------------------------------------------------
def test_red_agent_initialization(mock_db_session, memory_store):
    """Test RedAgent initializes with correct attack scenarios."""
    agent = RedAgent(
        db_session=mock_db_session,
        memory_store=memory_store,
    )

    assert agent.agent_id == "red-agent-1"
    assert agent.agent_type == "red"
    assert len(agent.attack_scenarios) == 4


def test_red_agent_perceive(mock_db_session, memory_store):
    """Test RedAgent.perceive() selects attack scenario."""
    agent = RedAgent(db_session=mock_db_session, memory_store=memory_store)
    perception = agent.perceive()

    assert "scenario" in perception
    assert perception["scenario"] in agent.attack_scenarios


def test_red_agent_run_basic(mock_db_session, memory_store):
    """Test RedAgent full run() cycle simulates an attack."""
    agent = RedAgent(db_session=mock_db_session, memory_store=memory_store)

    result = agent.run()

    assert "status" in result
    assert agent.is_running == False


# ------------------------------------------------------------------
# Test InstitutionalAgent (Momentum Block Trading)
# ------------------------------------------------------------------
def test_institutional_agent_initialization(mock_db_session, memory_store):
    """Test InstitutionalAgent initializes with correct parameters."""
    agent = InstitutionalAgent(
        db_session=mock_db_session,
        memory_store=memory_store,
        account_id=100,
        symbol="MSFT",
    )

    assert agent.agent_id == "institutional-agent-1"
    assert agent.agent_type == "institutional"
    assert agent.account_id == 100
    assert agent.symbol == "MSFT"


@patch("agenticAi.institutionalAgent.institutional.MarketDataTool")
def test_institutional_agent_perceive(mock_market_tool, mock_db_session, memory_store):
    """Test InstitutionalAgent.perceive() gets market data."""
    mock_market_instance = Mock()
    mock_market_instance.get_latest_price = Mock(return_value=150.0)
    mock_market_tool.return_value = mock_market_instance

    agent = InstitutionalAgent(db_session=mock_db_session, memory_store=memory_store)
    perception = agent.perceive()

    assert "price" in perception
    assert perception["price"] == 150.0


def test_institutional_agent_run_basic(mock_db_session, memory_store):
    """Test InstitutionalAgent full run() cycle."""
    agent = InstitutionalAgent(db_session=mock_db_session, memory_store=memory_store)

    result = agent.run()

    assert "status" in result
    assert agent.is_running == False


# ------------------------------------------------------------------
# Test RetailAgentA (Buy-the-Dip Value Strategy)
# ------------------------------------------------------------------
def test_retail_agent_a_initialization(mock_db_session, memory_store):
    """Test RetailAgentA initializes with value strategy parameters."""
    agent = RetailAgentA(
        db_session=mock_db_session,
        memory_store=memory_store,
        account_id=2,
        symbol="AAPL",
    )

    assert agent.agent_id == "retail-agent-a-1"
    assert agent.agent_type == "retail_a"
    assert agent.account_id == 2
    assert agent.symbol == "AAPL"


@patch("agenticAi.retailAgentA.retail_a.MarketDataTool")
@patch("agenticAi.retailAgentA.retail_a.PortfolioTool")
def test_retail_agent_a_perceive(mock_portfolio, mock_market, mock_db_session, memory_store):
    """Test RetailAgentA.perceive() gathers price and order data."""
    mock_market_instance = Mock()
    mock_market_instance.get_latest_price = Mock(return_value=140.0)
    mock_market.return_value = mock_market_instance

    mock_portfolio_instance = Mock()
    mock_portfolio_instance.get_order_count = Mock(return_value=5)
    mock_portfolio.return_value = mock_portfolio_instance

    agent = RetailAgentA(db_session=mock_db_session, memory_store=memory_store)
    perception = agent.perceive()

    assert "price" in perception
    assert "order_count" in perception
    assert perception["price"] == 140.0


def test_retail_agent_a_run_basic(mock_db_session, memory_store):
    """Test RetailAgentA full run() cycle."""
    agent = RetailAgentA(db_session=mock_db_session, memory_store=memory_store)

    result = agent.run()

    assert "status" in result
    assert agent.is_running == False


# ------------------------------------------------------------------
# Test RetailAgentB (Momentum FOMO Strategy)
# ------------------------------------------------------------------
def test_retail_agent_b_initialization(mock_db_session, memory_store):
    """Test RetailAgentB initializes with momentum parameters."""
    agent = RetailAgentB(
        db_session=mock_db_session,
        memory_store=memory_store,
        account_id=3,
        symbol="TSLA",
    )

    assert agent.agent_id == "retail-agent-b-1"
    assert agent.agent_type == "retail_b"
    assert agent.account_id == 3
    assert agent.symbol == "TSLA"


@patch("agenticAi.retailAgentB.retail_b.MarketDataTool")
def test_retail_agent_b_perceive(mock_market, mock_db_session, memory_store):
    """Test RetailAgentB.perceive() gathers momentum indicators."""
    mock_market_instance = Mock()
    mock_market_instance.get_latest_price = Mock(return_value=200.0)
    mock_market.return_value = mock_market_instance

    agent = RetailAgentB(db_session=mock_db_session, memory_store=memory_store)
    perception = agent.perceive()

    assert "price" in perception
    assert perception["price"] == 200.0


def test_retail_agent_b_run_basic(mock_db_session, memory_store):
    """Test RetailAgentB full run() cycle."""
    agent = RetailAgentB(db_session=mock_db_session, memory_store=memory_store)

    result = agent.run()

    assert "status" in result
    assert agent.is_running == False


# ------------------------------------------------------------------
# Integration Test: Multi-Agent Simulation
# ------------------------------------------------------------------
def test_multi_agent_simulation(mock_db_session, memory_store, mock_ollama_client):
    """Test all agents can run together in a simulated environment."""
    agents = [
        BlueAgent(db_session=mock_db_session, memory_store=memory_store, ollama_client=mock_ollama_client),
        RedAgent(db_session=mock_db_session, memory_store=memory_store, ollama_client=mock_ollama_client),
        InstitutionalAgent(db_session=mock_db_session, memory_store=memory_store),
        RetailAgentA(db_session=mock_db_session, memory_store=memory_store),
        RetailAgentB(db_session=mock_db_session, memory_store=memory_store),
    ]

    results = []
    for agent in agents:
        result = agent.run()
        results.append(result)
        assert "status" in result
        assert agent.is_running == False

    # All agents should have logged actions to DB
    assert mock_db_session.add.call_count >= len(agents)
    assert mock_db_session.commit.call_count >= len(agents)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
