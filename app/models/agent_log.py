from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, UTC
from app.database import Base


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)

    # 문자열 컬럼들에 길이 지정
    agent_id = Column(String(50), nullable=False)        # 에이전트 ID
    agent_type = Column(String(50), nullable=False)      # red / blue / institutional 등
    action = Column(String(100), nullable=False)         # 수행한 액션 이름

    result = Column(Text, nullable=True)                 # 긴 결과/로그는 Text 유지
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))