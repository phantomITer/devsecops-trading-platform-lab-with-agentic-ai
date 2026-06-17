from __future__ import annotations

from typing import Optional, Dict, Any, List
from datetime import datetime, UTC
import logging

logger = logging.getLogger(__name__)


class AlertTool:
    """
    Phase 2 - Agentic AI Core: tools/alert.py
    Creates and persists security events / alerts to the trading platform DB.

    Used by BlueAgent and RedAgent inside their act() method to raise
    detected anomalies or attack simulations as SecurityEvent records.
    """

    VALID_SEVERITIES = {"low", "medium", "high", "critical"}
    VALID_EVENT_TYPES = {
        "anomaly",
        "intrusion",
        "fraud",
        "ddos",
        "insider_threat",
        "data_exfiltration",
        "unauthorized_access",
        "simulation",
        "info",
    }

    def __init__(self, db_session=None):
        self.db = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_alert(
        self,
        event_type: str,
        severity: str,
        source: str,
        description: str,
    ) -> Dict[str, Any]:
        """
        Persist a security alert to the security_events table.

        Args:
            event_type: Type of event (e.g., "anomaly", "fraud").
            severity: "low" | "medium" | "high" | "critical".
            source: Origin of the alert (e.g., "blue-agent-1").
            description: Human-readable description of the event.

        Returns:
            Dict with 'success', 'event_id', and 'message'.
        """
        if severity not in self.VALID_SEVERITIES:
            return {"success": False, "message": f"Invalid severity: {severity}"}
        if self.db is None:
            # Graceful degradation: just log
            self.logger.warning(
                "[AlertTool] No DB session. Alert: [%s/%s] %s - %s",
                event_type, severity, source, description,
            )
            return {"success": False, "message": "No DB session; alert logged only"}

        try:
            from app.models.security_event import SecurityEvent
            event = SecurityEvent(
                event_type=event_type,
                severity=severity,
                source=source,
                description=description,
            )
            self.db.add(event)
            self.db.commit()
            self.db.refresh(event)
            self.logger.info(
                "[AlertTool] Created SecurityEvent id=%s type=%s severity=%s source=%s",
                event.id, event_type, severity, source,
            )
            return {"success": True, "event_id": event.id, "message": "Alert created"}
        except Exception as exc:
            self.db.rollback()
            self.logger.error("[AlertTool] create_alert error: %s", exc)
            return {"success": False, "message": str(exc)}

    def get_recent_alerts(
        self,
        limit: int = 20,
        severity: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve recent security events from DB, optionally filtered.
        Returns list of dicts, empty list on error or no DB.
        """
        if self.db is None:
            return []
        try:
            from app.models.security_event import SecurityEvent
            from sqlalchemy import desc
            q = self.db.query(SecurityEvent)
            if severity:
                q = q.filter(SecurityEvent.severity == severity)
            if event_type:
                q = q.filter(SecurityEvent.event_type == event_type)
            rows = q.order_by(desc(SecurityEvent.created_at)).limit(limit).all()
            return [
                {
                    "id": r.id,
                    "event_type": r.event_type,
                    "severity": r.severity,
                    "source": r.source,
                    "description": r.description,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ]
        except Exception as exc:
            self.logger.error("[AlertTool] get_recent_alerts error: %s", exc)
            return []

    def count_alerts_by_severity(self) -> Dict[str, int]:
        """Return counts per severity level for dashboard/reporting."""
        counts = {s: 0 for s in self.VALID_SEVERITIES}
        if self.db is None:
            return counts
        try:
            from app.models.security_event import SecurityEvent
            from sqlalchemy import func
            rows = (
                self.db.query(SecurityEvent.severity, func.count(SecurityEvent.id))
                .group_by(SecurityEvent.severity)
                .all()
            )
            for severity, count in rows:
                if severity in counts:
                    counts[severity] = count
        except Exception as exc:
            self.logger.error("[AlertTool] count_alerts_by_severity error: %s", exc)
        return counts
