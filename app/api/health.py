from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

_agent_heartbeats: dict = {}

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": "DevSecOps Trading Platform",
        "timestamp": datetime.now().isoformat(),
    }

@router.post("/health/agents/{agent_id}/heartbeat")
def agent_heartbeat(agent_id: str):
    _agent_heartbeats[agent_id] = datetime.now().isoformat()
    return {"status": "ok", "agent_id": agent_id}

@router.get("/health/agents")
def get_agents_status():
    agent_ids = ["red", "blue", "institutional", "retail_a", "retail_b"]
    result = {}
    for agent_id in agent_ids:
        last = _agent_heartbeats.get(agent_id)
        result[agent_id] = {"online": last is not None, "last_seen": last or "never"}
    return {"agents": result}