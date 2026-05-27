from datetime import datetime

from sqlalchemy.orm import Session

from app.repository.sla_tracking_repository import (
    SLATrackingRepository,
)

from app.tasks.escalation_tasks import (
    create_auto_escalation_task,
)

from app.services.sla_tracking_service import (
    SLATrackingService,

)
from app.models.approval import Approval
from app.models.task import Task


class SLABreachService:

    @staticmethod
    def process_sla_breaches(
        db: Session,
    ):
        overdue_slas = SLATrackingService.get_overdue_active_slas(db)

        breached_records = []

        for sla in overdue_slas:

            sla.status = "BREACHED"

            sla.breach_reason = "SLA due time exceeded"

            sla.updated_at = datetime.utcnow()

            updated_sla = SLATrackingRepository.update(
                db,
                sla,
            )

            breached_records.append(updated_sla)

            if sla.module_name.lower() == "task":
                task = db.query(Task).filter(Task.id == sla.record_id).first()
                if task:
                    task.sla_status = "BREACHED"
                    task.is_sla_breached = True
                    db.commit()

            if sla.module_name.lower() == "approval":
                approval = db.query(Approval).filter(Approval.id == sla.record_id).first()
                if approval:
                    approval.sla_status = "BREACHED"
                    db.commit()

            # trigger escalation
            if sla.module_name.lower() == "approval":
                create_auto_escalation_task.delay(
                    approval_id=sla.record_id,
                    escalated_from=1,
                    escalated_to=2,
                    reason="Approval breached SLA time",
                )
            
            # trigger notifications

        return breached_records
