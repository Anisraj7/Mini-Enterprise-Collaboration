from app.core.celery_app import (
    celery_app,
)

from app.db.database import SessionLocal

from app.services.sla_breach_service import (
    SLABreachService,
)


@celery_app.task(
    name="app.tasks.sla_tasks.check_sla_breaches_task"
)
def check_sla_breaches_task():

    db = SessionLocal()

    try:

        breached_records = (
            SLABreachService.process_sla_breaches(
                db
            )
        )

        print(
            f"Processed {len(breached_records)} breached SLA records"
        )

    finally:
        db.close()