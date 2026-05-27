from sqlalchemy.orm import Session

from app.models.activity_log import (
    ActivityLog,
)

from app.models.audit_log import (
    AuditLog,
)


def record_event(
    db: Session,
    *,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    organization_id: int | None = None,
) -> None:

    # =====================================
    # ACTIVITY LOG
    # =====================================
    activity_log = ActivityLog(

        user_id=user_id,

        action=action,

        entity_type=entity_type,

        entity_id=entity_id,

        organization_id=organization_id,
    )

    db.add(activity_log)

    # =====================================
    # AUDIT LOG
    # =====================================
    audit_log = AuditLog(

        user_id=user_id,

        organization_id=organization_id,

        # =====================================
        # FIXED FIELD NAMES
        # =====================================
        module_name=entity_type,

        action_type=action,

        record_id=entity_id,
    )

    db.add(audit_log)

    db.commit()