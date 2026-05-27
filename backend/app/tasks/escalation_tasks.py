from app.core.celery_app import (
    celery_app,
)

from app.db.database import SessionLocal

from app.services.approval_escalation_service import (
    ApprovalEscalationService,
)

from app.tasks.notification_tasks import (
    send_notification_task,
)


@celery_app.task(name="app.tasks.escalation_tasks.create_auto_escalation_task")
def create_auto_escalation_task(
    approval_id: int,
    escalated_from: int,
    escalated_to: int,
    reason: str,
):

    db = SessionLocal()

    try:

        ApprovalEscalationService.create_escalation(
            db=db,
            approval_id=approval_id,
            escalated_from=escalated_from,
            escalated_to=escalated_to,
            reason=reason,
        )

        send_notification_task.delay(
            user_id=escalated_to,
            title="Approval Escalated",
            message=f"Approval {approval_id} has been escalated to you",
            notification_type="ESCALATION",
            priority="HIGH",
        )

    finally:
        db.close()
