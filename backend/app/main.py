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
from app.db.database import Base, engine
from app.db.schema_compat import ensure_phase9_schema
from app.middleware.audit_middleware import AuditMiddleware

from app.routers import (
    activity,
    approval,
    approval_delegation_router,
    approval_escalation_router,
    audit,
    auth,
    channel,
    channel_member,
    comments,
    dashboard,
    document,
    kanban,
    notification,
    notification_preference_router,
    oAuth,
    payment,
    sla_rule,
    sla_tracking,
    tasks,
    tenant,
    tenant_collab,
    tenant_collab_usage,
    tenant_onboarding,
    users,
    websocket,
    workspace,
    workspace_member,
)
from app.routers import approval_document, channel_message, channel_task, task_document, workspace_message, workspace_task

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("mini_enterprise")

app = FastAPI(title="Mini Enterprise Collaboration Workflow")

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)

app.state.limiter = limiter

Base.metadata.create_all(bind=engine)
ensure_phase9_schema(engine)

# Core Routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(kanban.router)
app.include_router(comments.router)
app.include_router(approval.router)
app.include_router(dashboard.router)
app.include_router(activity.router)
app.include_router(document.router)
app.include_router(audit.router)
app.include_router(notification.router)
app.include_router(websocket.router)
app.include_router(oAuth.router)
app.include_router(payment.router)
app.include_router(sla_tracking.router)
app.include_router(sla_rule.router)

# Approval Extensions
app.include_router(approval_escalation_router.router)
app.include_router(notification_preference_router.router)
app.include_router(approval_delegation_router.router)

# Middleware
app.add_middleware(AuditMiddleware)

# Organization Routes
app.include_router(
    tenant_onboarding.router,
    prefix="/organizations",
    tags=["Organization Onboarding"]
)

app.include_router(
    tenant_collab.router,
    prefix="/organizations",
    tags=["Organization Collaboration Settings"]
)

app.include_router(
    tenant_collab_usage.router,
    prefix="/organizations",
    tags=["Organization Usage"]
)

app.include_router(
    tenant.router,
    prefix="/organizations",
    tags=["Organizations"]
)

# Workspace Routes
app.include_router(
    workspace.router,
    prefix="/workspaces",
    tags=["Workspaces"]
)

app.include_router(
    workspace_member.router,
    prefix="/workspaces",
    tags=["Workspace Members"]
)

# Channel Routes
app.include_router(
    channel.router,
    prefix="/channels",
    tags=["Channels"]
)

app.include_router(
    channel_member.router,
    prefix="/channels",
    tags=["Channel Members"]
)

app.include_router(
    workspace_message.router
)

app.include_router(
    channel_message.router
)

app.include_router(
    task_document.router
)

app.include_router(
    approval_document.router
)

app.include_router(
    workspace_task.router
)

app.include_router(
    channel_task.router
)

add_pagination(app)

uploads_dir = Path(__file__).resolve().parents[2] / "uploads"
uploads_dir.mkdir(exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=uploads_dir),
    name="uploads"
)

@app.middleware("http")
async def log_requests(request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)

    logger.info(
        "%s %s -> %s %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        (time.perf_counter() - started_at) * 1000,
    )

    return response

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler #type: ignore
)

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)