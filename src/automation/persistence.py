import json
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.mongo_client import ops_events, chief_aim as chief_aim_coll
from src.core.models import AuditLog, KPIRecord

# --------------------------
#   MONGO OPERATIONS
# --------------------------

def log_ops_event(event_type: str, payload: dict | None = None):
    """Insert an operational event (scheduler, agent, system) into MongoDB."""
    doc = {
        "event_type": event_type,
        "payload": payload or {},
        "ts": datetime.utcnow()
    }
    ops_events.insert_one(doc)
    return str(doc["_id"])


def update_chief_aim_reviewed():
    """Mark Chief Aim as reviewed in MongoDB."""
    chief_aim_coll.update_one(
        {"_id": "current"},
        {"$set": {"last_reviewed_at": datetime.utcnow()}},
        upsert=True
    )


# --------------------------
#   POSTGRES OPERATIONS
# --------------------------

def write_audit_log(db: Session, category: str, action: str, status: str, detail: dict | None = None):
    """Insert an audit trail entry into Postgres."""
    entry = AuditLog(
        category=category,
        action=action,
        status=status,
        detail=json.dumps(detail or {})
    )
    db.add(entry)
    db.commit()
    return entry.id


def bump_kpi(db: Session, category: str, metric: str, amount: float = 1.0):
    """Increment KPI counters."""
    entry = KPIRecord(
        category=category,
        metric=metric,
        value=amount
    )
    db.add(entry)
    db.commit()
    return entry.id
