
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AgentLogCreate(BaseModel):
    agent_id: str
    agent_type: str
    action: str
    result: Optional[str] = None

class AgentLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    agent_id: str
    agent_type: str
    action: str
    result: Optional[str]
    created_at: datetime
