from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page
from fastapi_pagination import paginate
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.sla_tracking import (
    SLATrackingResponse,
)

from app.services.sla_tracking_service import (
    SLATrackingService,
)

router = APIRouter(
    prefix="/sla-tracking",
    tags=["SLA Tracking"],
)


# POST Routes (specific)
@router.post(
    "/tasks/{task_id}",
    response_model=SLATrackingResponse,
)
def start_task_sla_tracking(
    task_id: int,
    priority: str,
    db: Session = Depends(get_db),
):
    return (
        SLATrackingService.start_sla_tracking(
            db,
            "Task",
            task_id,
            priority,
        )
    )


@router.post(
    "/approvals/{approval_id}",
    response_model=SLATrackingResponse,
)
def start_approval_sla_tracking(
    approval_id: int,
    priority: str,
    db: Session = Depends(get_db),
):
    return (
        SLATrackingService.start_sla_tracking(
            db,
            "Approval",
            approval_id,
            priority,
        )
    )


# GET Routes (specific literal paths first)
@router.get(
    "/active",
    response_model=Page[SLATrackingResponse],
)
def get_active_sla(
    db: Session = Depends(get_db),
):
    return paginate(SLATrackingService.get_active_sla(db))


@router.get(
    "/breached",
    response_model=Page[SLATrackingResponse],
)
def get_breached_sla(
    db: Session = Depends(get_db),
):
    return paginate(SLATrackingService.get_breached_sla(db))


@router.get(
    "/completed",
    response_model=Page[SLATrackingResponse],
)
def get_completed_sla(
    db: Session = Depends(get_db),
):
    return paginate(SLATrackingService.get_completed_sla(db))


# GET Routes (specific path parameters)
@router.get(
    "/record/{module_name}/{record_id}",
    response_model=SLATrackingResponse,
)
def get_sla_record(
    module_name: str,
    record_id: int,
    db: Session = Depends(get_db),
):
    return SLATrackingService.get_sla_record(
        db,
        module_name,
        record_id,
    )


@router.get(
    "/module/{module_name}",
    response_model=Page[SLATrackingResponse],
)
def get_sla_by_module(
    module_name: str,
    db: Session = Depends(get_db),
):
    return paginate(SLATrackingService.get_by_module(
        db,
        module_name,
    ))


# PUT Routes
@router.put(
    "/{tracking_id}/complete",
    response_model=SLATrackingResponse,
)
def complete_sla(
    tracking_id: int,
    db: Session = Depends(get_db),
):
    return SLATrackingService.complete_sla(
        db,
        tracking_id,
    )


# Generic POST Route (least specific)
@router.post(
    "/{module_name}/{record_id}",
    response_model=SLATrackingResponse,
)
def start_sla_tracking(
    module_name: str,
    record_id: int,
    priority: str,
    db: Session = Depends(get_db),
):
    return (
        SLATrackingService.start_sla_tracking(
            db,
            module_name,
            record_id,
            priority,
        )
    )
