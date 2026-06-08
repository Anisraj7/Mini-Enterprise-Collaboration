from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.cache import (
    cache_get,
    cache_set,
)

from app.models.activity_log import ActivityLog

from app.repository.activity_repository import (
    activity_logs_query,
)


def get_activity_logs_service(
    db: Session,
    current_user,
):

    cache_key = (
        f"activity:list:"
        f"user:{current_user.id}:"
        f"role:{current_user.role}"
    )

    cached = cache_get(cache_key)

    if cached:
        return cached

    query = activity_logs_query(
        db,
        current_user,
    )

    query = query.order_by(
        ActivityLog.created_at.desc()
    )

    result = paginate(db, query)

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result
