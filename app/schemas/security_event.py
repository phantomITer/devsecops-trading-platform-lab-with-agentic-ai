
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SecurityEventCreate(BaseModel):
    event_type: str
    severity: str
    source: Optional[str] = None
    description: Optional[str] = None

class SecurityEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_type: str
    severity: str
    source: Optional[str]
    description: Optional[str]
    created_at: datetime
