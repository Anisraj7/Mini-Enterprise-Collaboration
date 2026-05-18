from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from app.core.cache import cache_get, cache_set
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.audit import AuditLog

router = APIRouter(prefix="/audit-logs", tags=["Audit"])


@router.get("/")
def get_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cache_key = f"audit:list:user:{user.id}:role:{user.role}:page:{page}:limit:{limit}"
    cached = cache_get(cache_key)
    if cached is not None:
        return cached

    skip = (page - 1) * limit

    query = db.query(AuditLog)
    if user.organization_id:
        query = query.filter(AuditLog.organization_id == user.organization_id)

    if user.role != "admin":
        query = query.filter(AuditLog.user_id == user.id)

    total = query.count()

    logs = (
        query
        .order_by(AuditLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
        "data": logs
    }
    result = jsonable_encoder(result)
    cache_set(cache_key, result)
    return result
