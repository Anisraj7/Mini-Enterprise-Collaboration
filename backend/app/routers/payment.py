from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentVerify

from app.services.payment_service import (
    create_order,
    get_current_subscription,
    verify_payment,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/create-order")
def create_payment(payload: PaymentCreate):
    return create_order(payload.plan)


@router.post("/verify")
def verify(
    payload: PaymentVerify,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return verify_payment(payload, user, db)


@router.get("/subscription")
def current_subscription(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_current_subscription(user, db)
