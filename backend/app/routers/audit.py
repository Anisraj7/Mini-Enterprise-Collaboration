from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from datetime import datetime

from sqlalchemy.orm import Session

from fastapi.encoders import (
    jsonable_encoder,
)

from app.core.cache import (
    cache_get,
    cache_set,
)

from app.core.dependencies import (
    get_current_user,
)

from app.db.database import (
    get_db,
)

from app.models.audit_log import (
    AuditLog,
)

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)

from app.core.permissions import (
    require_auditor_or_admin,
)


# =========================================
# GET AUDIT LOGS
# =========================================
@router.get("/")
def get_logs(
    page: int = Query(
        1,
        ge=1,
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
    ),
    module_name: str | None = None,
    action_type: str | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    
    require_auditor_or_admin(
        user
    )

    cache_key = (
        f"audit:list:"
        f"user:{user.id}:"
        f"role:{user.role}:"
        f"page:{page}:"
        f"limit:{limit}:"
        f"module:{module_name}:"
        f"action:{action_type}:"
        f"user_filter:{user_id}"
    )

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    skip = (page - 1) * limit

    query = db.query(AuditLog)

    # =====================================
    # ORGANIZATION FILTER
    # =====================================
    if user.organization_id:

        query = query.filter(
            AuditLog.organization_id
            == user.organization_id
        )

    # =====================================
    # NON-ADMIN RESTRICTION
    # =====================================
    if user.role != "admin":

        query = query.filter(
            AuditLog.user_id
            == user.id
        )

    # =====================================
    # OPTIONAL FILTERS
    # =====================================
    if module_name:

        query = query.filter(
            AuditLog.module_name
            == module_name
        )

    if action_type:

        query = query.filter(
            AuditLog.action_type
            == action_type
        )

    if user_id and user.role == "admin":

        query = query.filter(
            AuditLog.user_id
            == user_id
        )

    total = query.count()

    logs = (
        query
        .order_by(
            AuditLog.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (
            total + limit - 1
        ) // limit,
        "data": logs,
    }

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result


@router.get("")
def get_logs_no_slash(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    module_name: str | None = None,
    action_type: str | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_logs(
        page=page,
        limit=limit,
        module_name=module_name,
        action_type=action_type,
        user_id=user_id,
        db=db,
        user=user,
    )


@router.get("/date-range")
def get_logs_by_date_range(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    query = db.query(AuditLog).filter(
        AuditLog.created_at >= start_date,
        AuditLog.created_at <= end_date,
    )

    if user.organization_id:
        query = query.filter(AuditLog.organization_id == user.organization_id)

    if user.role != "admin":
        query = query.filter(AuditLog.user_id == user.id)

    return query.order_by(AuditLog.created_at.desc()).all()


@router.get("/module/{module_name}")
def get_logs_by_module(
    module_name: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    query = db.query(AuditLog).filter(AuditLog.module_name == module_name)

    if user.organization_id:
        query = query.filter(AuditLog.organization_id == user.organization_id)

    if user.role != "admin":
        query = query.filter(AuditLog.user_id == user.id)

    return query.order_by(AuditLog.created_at.desc()).all()


@router.get("/user/{user_id}")
def get_logs_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    if user.role != "admin" and user.id != user_id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    query = db.query(AuditLog).filter(AuditLog.user_id == user_id)

    if user.organization_id:
        query = query.filter(AuditLog.organization_id == user.organization_id)

    return query.order_by(AuditLog.created_at.desc()).all()


@router.get("/{audit_log_id}")
def get_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_auditor_or_admin(user)

    query = db.query(AuditLog).filter(AuditLog.id == audit_log_id)

    if user.organization_id:
        query = query.filter(AuditLog.organization_id == user.organization_id)

    if user.role != "admin":
        query = query.filter(AuditLog.user_id == user.id)

    log = query.first()

    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")

    return log
