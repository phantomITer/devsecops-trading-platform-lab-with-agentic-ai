from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, UTC
from app.database import Base


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)

    # 문자열 컬럼들에 길이 지정
    event_type = Column(String(50), nullable=False)   # ex) LOGIN_FAILED, SQLI_DETECTED
    severity = Column(String(20), nullable=False)     # ex) LOW, MEDIUM, HIGH
    source = Column(String(50), nullable=True)        # ex) red_agent, blue_agent, api

    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))