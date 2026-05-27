from celery import Celery

celery_app = Celery(
    "mecw_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "check-sla-breaches-every-minute": {
        "task": "app.tasks.sla_tasks.check_sla_breaches_task",
        "schedule": 60.0,
    },
}

celery_app.autodiscover_tasks(
    [
        "app.tasks",
    ]
)