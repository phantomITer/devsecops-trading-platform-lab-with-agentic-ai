
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.agent_log import AgentLogCreate, AgentLogResponse
from app.services.agent_log_service import create_agent_log, get_agent_logs

router = APIRouter(prefix="/agent-logs", tags=["agent-logs"])

@router.get("/", response_model=List[AgentLogResponse])
def list_logs(db: Session = Depends(get_db)):
    return get_agent_logs(db)

@router.post("/", response_model=AgentLogResponse, status_code=201)
def new_log(data: AgentLogCreate, db: Session = Depends(get_db)):
    return create_agent_log(db, data)
