from sqlalchemy import func
from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from app.core.cache import (
    cache_get,
    cache_set,
)

from app.models.task import Task

from app.services.ai_service import generate_ai_summary

from app.repository.dashboard_repository import (
    visible_tasks_query,
    approval_query,
    grouped_task_status_query,
    grouped_approval_status_query,
)

from app.services.task_service import WORKFLOW_STATUSES


def summary_service(
    db: Session,
    user,
):

    cache_key = f"dashboard:summary:{user.id}"

    cached = cache_get(cache_key)

    if cached:
        return cached

    query = visible_tasks_query(
        db,
        user,
    )

    total_tasks = query.count()

    grouped = grouped_task_status_query(
        query
    )

    status_counts = {
        status_name: 0
        for status_name in WORKFLOW_STATUSES
    }

    status_counts.update(
        {
            status_name: count
            for status_name, count in grouped
        }
    )

    approval_count = approval_query(
        db,
        user,
    ).count()

    tasks = query.all()

    result = {
        "total_tasks": total_tasks,
        "tasks_by_status": status_counts,
        "status_distribution": status_counts,
        "completed_tasks": status_counts.get("done", 0),
        "pending_approvals": approval_count,
        **generate_ai_summary(tasks),
    }

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result


def task_distribution_service(
    db: Session,
    user,
):

    cache_key = f"dashboard:distribution:{user.id}"

    cached = cache_get(cache_key)

    if cached:
        return cached

    query = visible_tasks_query(
        db,
        user,
    )

    data = grouped_task_status_query(
        query
    )

    counts = {
        status_name: 0
        for status_name in WORKFLOW_STATUSES
    }

    counts.update(
        {
            status_name: count
            for status_name, count in data
        }
    )

    result = [
        {
            "status": status_name,
            "count": count,
        }
        for status_name, count in counts.items()
    ]

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result


def approvals_service(
    db: Session,
    user,
):

    cache_key = f"dashboard:approvals:{user.id}"

    cached = cache_get(cache_key)

    if cached:
        return cached

    data = grouped_approval_status_query(
        db,
        user,
    )

    result = [
        {
            "status": status_name,
            "count": count,
        }
        for status_name, count in data
    ]

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result


def ai_summary_service(
    db: Session,
    user,
):

    cache_key = f"dashboard:ai:{user.id}"

    cached = cache_get(cache_key)

    if cached:
        return cached

    tasks = (
        visible_tasks_query(
            db,
            user,
        )
        .all()
    )

    result = generate_ai_summary(tasks)

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result