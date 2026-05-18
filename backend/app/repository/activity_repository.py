from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.models.activity_log import ActivityLog


def activity_logs_query(
    db: Session,
    current_user,
):

    query = db.query(ActivityLog)

    if current_user.organization_id:
        query = query.filter(
            ActivityLog.organization_id
            == current_user.organization_id
        )

    return query.options(
        joinedload(ActivityLog.user)
    )
