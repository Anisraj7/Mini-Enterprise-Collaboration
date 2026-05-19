from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.models import User

from app.schemas.payment import (
    PaymentCreate,
    PaymentVerify,
)

# ===================================
# RAZORPAY
# ===================================
from app.services.razorpay_service import (
    create_order,
    verify_payment,
    get_current_subscription,
)

# ===================================
# STRIPE
# ===================================
from app.services.stripe_service import (
    create_checkout_session,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


# ===================================
# CREATE PAYMENT
# ===================================
@router.post("/create-payment")
def create_payment(
    payload: PaymentCreate,
):

    provider = payload.provider.lower()

    # -------------------------------
    # RAZORPAY
    # -------------------------------
    if provider == "razorpay":

        return create_order(
            payload.plan
        )

    # -------------------------------
    # STRIPE
    # -------------------------------
    elif provider == "stripe":

        return create_checkout_session(
            payload.plan
        )

    return {
        "success": False,
        "message":
            "Invalid payment provider",
    }


# ===================================
# VERIFY RAZORPAY PAYMENT
# ===================================
@router.post("/verify")
def verify(
    payload: PaymentVerify,

    db: Session = Depends(get_db),

    user: User = Depends(
        get_current_user
    ),
):

    return verify_payment(
        payload,
        user,
        db,
    )


# ===================================
# GET SUBSCRIPTION
# ===================================
@router.get("/subscription")
def current_subscription(
    db: Session = Depends(get_db),

    user: User = Depends(
        get_current_user
    ),
):

    return get_current_subscription(
        user,
        db,
    )