
from sqlalchemy.orm import Session
from app.models.security_event import SecurityEvent
from app.schemas.security_event import SecurityEventCreate

def create_security_event(db: Session, data: SecurityEventCreate) -> SecurityEvent:
    event = SecurityEvent(
        event_type=data.event_type,
        severity=data.severity,
        source=data.source,
        description=data.description,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_security_events(db: Session):
    return db.query(SecurityEvent).all()
