from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
)

from app.core.permissions import (
    require_auditor_or_admin,
)

from app.db.database import (
    get_db,
)

from app.models.audit_log import (
    AuditLog,
)
from app.schemas.audit_log import AuditLogOut

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


# =========================================
# GET AUDIT LOGS
# =========================================
@router.get("/", response_model=Page[AuditLogOut])
def get_logs(
    module_name: str | None = None,
    action_type: str | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    query = select(AuditLog)

    # =====================================
    # ORGANIZATION FILTER
    # =====================================
    if user.organization_id:
        query = query.where(
            AuditLog.organization_id
            == user.organization_id
        )

    # =====================================
    # NON-ORG-ADMIN RESTRICTION
    # =====================================
    if user.role != "organization_admin":
        query = query.where(
            AuditLog.user_id
            == user.id
        )

    # =====================================
    # OPTIONAL FILTERS
    # =====================================
    if module_name:
        query = query.where(
            AuditLog.module_name
            == module_name
        )

    if action_type:
        query = query.where(
            AuditLog.action_type
            == action_type
        )

    if (
        user_id and
        user.role == "organization_admin"
    ):
        query = query.where(
            AuditLog.user_id
            == user_id
        )

    return paginate(
        db,
        query.order_by(AuditLog.created_at.desc())
    )


@router.get("", response_model=Page[AuditLogOut])
def get_logs_no_slash(
    module_name: str | None = None,
    action_type: str | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_logs(
        module_name=module_name,
        action_type=action_type,
        user_id=user_id,
        db=db,
        user=user,
    )


@router.get("/date-range", response_model=Page[AuditLogOut])
def get_logs_by_date_range(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    query = select(AuditLog).where(
        AuditLog.created_at >= start_date,
        AuditLog.created_at <= end_date,
    )

    if user.organization_id:
        query = query.where(
            AuditLog.organization_id
            == user.organization_id
        )

    if user.role != "organization_admin":
        query = query.where(
            AuditLog.user_id
            == user.id
        )

    return paginate(db, query.order_by(AuditLog.created_at.desc()))


@router.get("/module/{module_name}", response_model=Page[AuditLogOut])
def get_logs_by_module(
    module_name: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    query = select(AuditLog).where(
        AuditLog.module_name == module_name
    )

    if user.organization_id:
        query = query.where(
            AuditLog.organization_id
            == user.organization_id
        )

    if user.role != "organization_admin":
        query = query.where(
            AuditLog.user_id
            == user.id
        )

    return paginate(db, query.order_by(AuditLog.created_at.desc()))


@router.get("/user/{user_id}", response_model=Page[AuditLogOut])
def get_logs_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    if (
        user.role != "organization_admin"
        and user.id != user_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )

    query = select(AuditLog).where(
        AuditLog.user_id == user_id
    )

    if user.organization_id:
        query = query.where(
            AuditLog.organization_id
            == user.organization_id
        )

    return paginate(db, query.order_by(AuditLog.created_at.desc()))


@router.get("/{audit_log_id}", response_model=AuditLogOut)
def get_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    query = select(AuditLog).where(
        AuditLog.id == audit_log_id
    )

    if user.organization_id:
        query = query.where(
            AuditLog.organization_id
            == user.organization_id
        )

    if user.role != "organization_admin":
        query = query.where(
            AuditLog.user_id
            == user.id
        )

    log = db.execute(query).scalars().first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found",
        )

    return log
