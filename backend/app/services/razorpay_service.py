from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
)

from app.models.subscription import (
    Subscription,
)

import razorpay


# -----------------------------------
# RAZORPAY CLIENT
# -----------------------------------
client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_KEY_SECRET,
    )
)


# -----------------------------------
# PLAN CONFIGURATION
# -----------------------------------
PLAN_CREDITS = {
    "basic": 500,
    "silver": 1000,
    "gold": 10000,
}

PLAN_PRICES = {
    "basic": 0,
    "silver": 1499,
    "gold": 4999,
}


# -----------------------------------
# CREATE ORDER
# -----------------------------------
def create_order(plan: str):

    normalized_plan = (
        plan or "basic"
    ).lower()

    if normalized_plan not in PLAN_PRICES:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported subscription plan"
            ),
        )

    try:

        order = client.order.create(
            {
                "amount": (
                    PLAN_PRICES[
                        normalized_plan
                    ]
                    * 100
                ),
                "currency": "INR",
                "payment_capture": 1,
                "notes": {
                    "plan": normalized_plan,
                },
            }
        )

        return {
            "success": True,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "plan": normalized_plan,
            "credits": PLAN_CREDITS[
                normalized_plan
            ],
            "key": RAZORPAY_KEY_ID,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=(
                "Failed to create Razorpay order: "
                f"{str(exc)}"
            ),
        )


# -----------------------------------
# VERIFY PAYMENT
# -----------------------------------
def verify_payment(
    payload,
    user,
    db: Session,
):

    # VERIFY USER ORGANIZATION

    if not user.organization_id:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "User is not attached "
                "to an organization"
            ),
        )

    # VERIFY PLAN

    plan = (
        payload.plan or "basic"
    ).lower()

    if plan not in PLAN_CREDITS:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported subscription plan"
            ),
        )

    # VERIFY RAZORPAY SIGNATURE

    try:

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": (
                    payload.razorpay_order_id
                ),
                "razorpay_payment_id": (
                    payload.razorpay_payment_id
                ),
                "razorpay_signature": (
                    payload.razorpay_signature
                ),
            }
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment signature",
        )

    # PREVENT DUPLICATE PAYMENTS

    existing_payment = (
        db.execute(select(Subscription).where(
            Subscription.razorpay_payment_id
            == payload.razorpay_payment_id
        ))
        .scalars()
        .first()
    )

    if existing_payment:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already processed",
        )

    # GET EXISTING SUBSCRIPTION

    subscription = (
        db.execute(select(Subscription).where(
            Subscription.organization_id
            == user.organization_id
        ))
        .scalars()
        .first()
    )

    # CREATE NEW SUBSCRIPTION

    if not subscription:

        subscription = Subscription(
            organization_id=(
                user.organization_id
            ),
            credits=0,
            status="inactive",
        )

        db.add(subscription)

    # USE UTC NAIVE DATETIME
    now = datetime.utcnow()

    # UPDATE SUBSCRIPTION

    subscription.plan = plan

    # ADD CREDITS
    subscription.credits += (
        PLAN_CREDITS[plan]
    )

    subscription.status = "active"

    subscription.start_date = now

    subscription.end_date = (
        now + timedelta(days=30)
    )

    # STORE PAYMENT DETAILS

    subscription.razorpay_order_id = (
    payload.razorpay_order_id
    )

    subscription.razorpay_payment_id = (
        payload.razorpay_payment_id
    )

    db.commit()

    db.refresh(subscription)

    return {
        "success": True,
        "message": (
            "Payment verified and "
            "subscription activated"
        ),
        "subscription": {
            "plan": subscription.plan,
            "credits": subscription.credits,
            "status": subscription.status,
            "start_date": (
                subscription.start_date
            ),
            "end_date": (
                subscription.end_date
            ),
        },
    }


# -----------------------------------
# GET CURRENT SUBSCRIPTION
# -----------------------------------
def get_current_subscription(
    user,
    db: Session,
):

    if not user.organization_id:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "User is not attached "
                "to an organization"
            ),
        )

    subscription = (
        db.execute(select(Subscription).where(
            Subscription.organization_id
            == user.organization_id
        ))
        .scalars()
        .first()
    )

    # NO SUBSCRIPTION

    if not subscription:

        return {
            "plan": None,
            "credits": 0,
            "status": "inactive",
            "start_date": None,
            "end_date": None,
        }

    # UTC NAIVE DATETIME
    now = datetime.utcnow()

    end_date = subscription.end_date

    # FIX OFFSET-AWARE ISSUE

    if (
        end_date
        and end_date.tzinfo
        is not None
    ):
        end_date = end_date.replace(
            tzinfo=None
        )

    if (
        now.tzinfo
        is not None
    ):
        now = now.replace(
            tzinfo=None
        )

    # AUTO EXPIRE SUBSCRIPTION

    if end_date and end_date < now:

        subscription.status = "expired"

        db.commit()

        db.refresh(subscription)

    return {
        "plan": subscription.plan,
        "credits": subscription.credits,
        "status": subscription.status,
        "start_date": (
            subscription.start_date
        ),
        "end_date": (
            subscription.end_date
        ),
    }
