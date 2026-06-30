import logging
import os
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.rate_limit import limiter
from app.db.database import engine
from app.db.schema_compat import ensure_phase9_schema
from app.middleware.audit_middleware import AuditMiddleware

from app.routers import (
    activity,
    ai_meeting_summary,
    approval,
    approval_delegation_router,
    approval_document,
    approval_escalation_router,
    audit,
    auth,
    calender,
    channel,
    channel_member,
    channel_message,
    channel_task,
    comments,
    dashboard,
    document,
    kanban,
    meeting,
    meeting_attendee,
    meeting_note,
    notification,
    notification_preference_router,
    oAuth,
    payment,
    project,
    project_document,
    project_team,
    sla_rule,
    sla_tracking,
    task_document,
    tasks,
    team,
    team_member,
    tenant,
    tenant_collab,
    tenant_collab_usage,
    tenant_onboarding,
    users,
    websocket,
    workload,
    workspace,
    workspace_member,
    workspace_message,
    workspace_task,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("mini_enterprise")

app = FastAPI(title="Mini Enterprise Collaboration Workflow")

app.state.limiter = limiter

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key",
)

app.add_middleware(AuditMiddleware)

app.add_middleware(SlowAPIMiddleware)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_phase9_schema(engine)

# Core
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(kanban.router)
app.include_router(comments.router)
app.include_router(approval.router)
app.include_router(activity.router)
app.include_router(document.router)
app.include_router(audit.router)
app.include_router(notification.router)
app.include_router(websocket.router)
app.include_router(oAuth.router)
app.include_router(payment.router)
app.include_router(dashboard.router)
app.include_router(sla_tracking.router)
app.include_router(sla_rule.router)

# Approval
app.include_router(approval_escalation_router.router)
app.include_router(approval_delegation_router.router)
app.include_router(notification_preference_router.router)

# Organization
app.include_router(tenant.router, prefix="/organizations")
app.include_router(tenant_onboarding.router, prefix="/organizations")
app.include_router(tenant_collab.router, prefix="/organizations")
app.include_router(tenant_collab_usage.router, prefix="/organizations")

# Workspace
app.include_router(workspace.router, prefix="/workspaces")
app.include_router(workspace_member.router, prefix="/workspaces")

# Channel
app.include_router(channel.router, prefix="/channels")
app.include_router(channel_member.router, prefix="/channels")

# Collaboration
for router in (
    workspace_message.router,
    workspace_task.router,
    channel_message.router,
    channel_task.router,
    task_document.router,
    approval_document.router,
    team.router,
    team_member.router,
    project.router,
    project_team.router,
    project_document.router,
    meeting.router,
    meeting_attendee.router,
    meeting_note.router,
    ai_meeting_summary.router,
    calender.router,
    workload.router,
):
    app.include_router(router)

add_pagination(app)

uploads = Path(__file__).resolve().parents[2] / "uploads"
uploads.mkdir(exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=uploads),
    name="uploads",
)

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)

    logger.info(
        "%s %s -> %s %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        (time.perf_counter() - start) * 1000,
    )

    return response

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler, # type: ignore
)