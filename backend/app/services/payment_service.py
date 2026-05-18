import razorpay
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from app.core.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from app.models.subscription import Subscription

client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_KEY_SECRET
    )
)


PLAN_CREDITS = {
    "basic": 100,
    "silver": 1000,
    "gold": 10000,
}

PLAN_PRICES = {
    "basic": 499,
    "silver": 1499,
    "gold": 4999,
}


def create_order(plan: str):
    normalized_plan = (plan or "basic").lower()
    if normalized_plan not in PLAN_PRICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported subscription plan",
        )

    order = client.order.create({
        "amount": PLAN_PRICES[normalized_plan] * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        **order,
        "plan": normalized_plan,
        "credits": PLAN_CREDITS[normalized_plan],
    }


def verify_payment(payload, user, db):
    if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": payload.razorpay_order_id,
                "razorpay_payment_id": payload.razorpay_payment_id,
                "razorpay_signature": payload.razorpay_signature,
            })
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment signature",
            ) from exc

    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not attached to an organization",
        )

    plan = (payload.plan or "basic").lower()
    if plan not in PLAN_CREDITS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported subscription plan",
        )

    subscription = db.query(Subscription).filter(
        Subscription.organization_id == user.organization_id
    ).first()

    if not subscription:
        subscription = Subscription(
            organization_id=user.organization_id,
        )
        db.add(subscription)

    subscription.plan = plan
    subscription.credits = PLAN_CREDITS[plan]
    subscription.status = "active"
    subscription.start_date = datetime.utcnow()
    subscription.end_date = datetime.utcnow() + timedelta(days=30)
    db.commit()
    db.refresh(subscription)

    return {
        "message": "Payment verified and subscription activated",
        "subscription": {
            "plan": subscription.plan,
            "credits": subscription.credits,
            "status": subscription.status,
            "end_date": subscription.end_date,
        },
    }


def get_current_subscription(user, db):
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not attached to an organization",
        )

    subscription = db.query(Subscription).filter(
        Subscription.organization_id == user.organization_id
    ).first()

    if not subscription:
        return {
            "plan": None,
            "credits": 0,
            "status": "inactive",
            "end_date": None,
        }

    return {
        "plan": subscription.plan,
        "credits": subscription.credits,
        "status": subscription.status,
        "end_date": subscription.end_date,
    }
