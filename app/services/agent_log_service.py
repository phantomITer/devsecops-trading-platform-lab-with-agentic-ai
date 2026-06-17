
from sqlalchemy.orm import Session
from app.models.agent_log import AgentLog
from app.schemas.agent_log import AgentLogCreate

def create_agent_log(db: Session, data: AgentLogCreate) -> AgentLog:
    log = AgentLog(
        agent_id=data.agent_id,
        agent_type=data.agent_type,
        action=data.action,
        result=data.result,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_agent_logs(db: Session):
    return db.query(AgentLog).all()
