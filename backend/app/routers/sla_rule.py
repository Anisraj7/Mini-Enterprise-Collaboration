from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.sla_rule import (
    SLARuleCreate,
    SLARuleResponse,
    SLARuleUpdate,
)

from app.services.sla_service import (
    SLARuleService,
)

router = APIRouter(
    prefix="/sla-rules",
    tags=["SLA Rules"],
)

from app.core.permissions import (
    require_admin,
)


@router.post(
    "",
    response_model=SLARuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sla_rule(
    payload: SLARuleCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return SLARuleService.create_sla_rule(
        db=db,
        payload=payload,
        user_id=user.id,
    )


@router.get(
    "",
    response_model=list[SLARuleResponse],
)
def get_all_sla_rules(
    db: Session = Depends(get_db),
):
    return SLARuleService.get_all_sla_rules(db)


@router.get(
    "/{sla_rule_id}",
    response_model=SLARuleResponse,
)
def get_sla_rule_by_id(
    sla_rule_id: int,
    db: Session = Depends(get_db),
):
    return SLARuleService.get_sla_rule_by_id(
        db,
        sla_rule_id,
    )


@router.put(
    "/{sla_rule_id}",
    response_model=SLARuleResponse,
)
def update_sla_rule(
    sla_rule_id: int,
    payload: SLARuleUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return SLARuleService.update_sla_rule(
        db,
        sla_rule_id,
        payload,
    )


@router.delete(
    "/{sla_rule_id}",
)
def disable_sla_rule(
    sla_rule_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    SLARuleService.disable_sla_rule(
        db,
        sla_rule_id,
    )

    return {
        "message": "SLA rule disabled successfully"
    }
