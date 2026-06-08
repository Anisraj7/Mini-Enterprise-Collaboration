from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.models.user import User

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
    verify_stripe_payment,
)

# ===================================
# MODELS
# ===================================
from app.models.subscription import Subscription

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
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not attached to an organization",
        )

    provider = payload.provider.lower()
    plan = payload.plan.lower()

    # ===================================
    # FREE BASIC PLAN
    # ===================================
    if plan == "basic":

        from datetime import (
            datetime,
            timedelta,
            timezone,
        )

        subscription = (
            db.execute(select(Subscription).where(
                Subscription.organization_id
                == user.organization_id
            ))
            .scalars()
            .first()
        )

        # CREATE SUBSCRIPTION IF NOT EXISTS
        if not subscription:

            subscription = Subscription(
                organization_id=user.organization_id,
                credits=0,
            )

            db.add(subscription)

        now = datetime.now(timezone.utc)

        subscription.plan = "basic"
        subscription.status = "active"
        subscription.credits = 500
        subscription.start_date = now
        subscription.end_date = now + timedelta(days=30)

        db.commit()
        db.refresh(subscription)

        return {
            "success": True,
            "message": "Basic plan activated successfully",
            "subscription": {
                "plan": subscription.plan,
                "credits": subscription.credits,
                "status": subscription.status,
                "start_date": subscription.start_date,
                "end_date": subscription.end_date,
            },
        }

    # ===================================
    # RAZORPAY
    # ===================================
    if provider == "razorpay":

        return create_order(plan)

    # ===================================
    # STRIPE
    # ===================================
    elif provider == "stripe":

        return create_checkout_session(plan)

    return {
        "success": False,
        "message": "Invalid payment provider",
    }

# ===================================
# VERIFY RAZORPAY PAYMENT
# ===================================
@router.post("/verify")
def verify(
    payload: PaymentVerify,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    return verify_payment(
        payload,
        user,
        db,
    )


# ===================================
# VERIFY STRIPE PAYMENT
# ===================================
@router.post("/verify-stripe")
def verify_stripe(
    session_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Verify Stripe payment using session ID and add credits.
    Called after successful payment redirect.
    """
    return verify_stripe_payment(
        session_id,
        user,
        db,
    )


# ===================================
# GET SUBSCRIPTION
# ===================================
@router.get("/subscription")
def current_subscription(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    return get_current_subscription(
        user,
        db,
    )


# ===================================
# ACTIVATE SUBSCRIPTION (MANUAL BUTTON)
# ===================================
@router.post("/activate-plan")
def activate_plan(
    plan: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Manually activate a plan and add credits.
    This endpoint is for the activation button when payment system has issues.
    """
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not attached to an organization",
        )

    plan = (plan or "basic").lower()

    PLAN_CREDITS = {
        "basic": 500,
        "silver": 1000,
        "gold": 10000,
    }

    if plan not in PLAN_CREDITS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported subscription plan",
        )

    from datetime import datetime, timedelta, timezone

    subscription = (
        db.execute(
            select(Subscription).where(
                Subscription.organization_id == user.organization_id
            )
        )
        .scalars()
        .first()
    )

    if not subscription:
        subscription = Subscription(
            organization_id=user.organization_id,
            credits=0,
        )
        db.add(subscription)

    now = datetime.now(timezone.utc)

    subscription.plan = plan
    subscription.credits += PLAN_CREDITS[plan]
    subscription.status = "active"
    subscription.start_date = now
    subscription.end_date = now + timedelta(days=30)

    db.commit()
    db.refresh(subscription)

    return {
        "success": True,
        "message": f"Plan {plan} activated successfully",
        "subscription": {
            "plan": subscription.plan,
            "credits": subscription.credits,
            "status": subscription.status,
            "start_date": subscription.start_date,
            "end_date": subscription.end_date,
        },
    }
