
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, UTC
from app.database import Base

class AgentLog(Base):
    __tablename__ = "agent_logs"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, nullable=False)
    agent_type = Column(String, nullable=False)
    action = Column(String, nullable=False)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
