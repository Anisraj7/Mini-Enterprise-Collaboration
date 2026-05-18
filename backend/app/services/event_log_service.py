from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.models.audit import AuditLog


def record_event(
    db: Session,
    *,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    organization_id: int | None = None,
) -> None:
    db.add(
        ActivityLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            organization_id=organization_id,
        )
    )
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity=entity_type,
            entity_id=entity_id,
            organization_id=organization_id,
        )
    )
