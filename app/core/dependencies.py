from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import verify_api_key, decode_access_token
from app.database import SessionLocal
from typing import Optional

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_agent_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-API-Key header missing")
    agent_id = verify_api_key(x_api_key)
    if not agent_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return agent_id

bearer_scheme = HTTPBearer(auto_error=False)

async def verify_jwt_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return payload

AgentDep = Depends(verify_agent_api_key)
UserDep  = Depends(verify_jwt_token)
DBDep    = Depends(get_db)