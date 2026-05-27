import stripe
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import (
    STRIPE_SECRET_KEY,
    STRIPE_PUBLISHABLE_KEY,
)
from app.models.subscription import Subscription

stripe.api_key = STRIPE_SECRET_KEY


PLAN_PRICES = {
    "basic": 0,
    "silver": 1499,
    "gold": 4999,
}

PLAN_CREDITS = {
    "basic": 500,
    "silver": 1000,
    "gold": 10000,
}


def create_checkout_session(plan: str):

    plan = plan.lower()

    if plan not in PLAN_PRICES:
        raise HTTPException(status_code=400, detail="Invalid plan")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": f"{plan.title()} Plan",
                    },
                    "unit_amount": PLAN_PRICES[plan] * 100,
                },
                "quantity": 1,
            }
        ],
        success_url="http://localhost:5173/payment-success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:5173/billing",
        metadata={
            "plan": plan,
        },
    )

    return {
        "checkout_url": session.url,
        "public_key": STRIPE_PUBLISHABLE_KEY,
        "session_id": session.id,
    }


def verify_stripe_payment(session_id: str, user, db: Session):
    """
    Verify Stripe payment and add credits to subscription.
    """
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not attached to an organization",
        )

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID",
        )

    if session.payment_status != "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment not completed",
        )

    plan = (session.metadata.get("plan") or "basic").lower()

    if plan not in PLAN_CREDITS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan",
        )

    # Check for duplicate only if column exists
    try:
        existing_payment = (
            db.query(Subscription)
            .filter(Subscription.stripe_session_id == session_id)
            .first()
        )

        if existing_payment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already processed",
            )
    except Exception as e:
        if "stripe_session_id" in str(e):
            pass
        else:
            raise

    subscription = (
        db.query(Subscription)
        .filter(Subscription.organization_id == user.organization_id)
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
    
    # Try to store Stripe details if columns exist
    try:
        subscription.stripe_session_id = session_id
        subscription.stripe_payment_intent_id = session.payment_intent
    except Exception:
        pass

    db.commit()
    db.refresh(subscription)

    return {
        "success": True,
        "message": "Payment verified and subscription activated",
        "subscription": {
            "plan": subscription.plan,
            "credits": subscription.credits,
            "status": subscription.status,
            "start_date": subscription.start_date,
            "end_date": subscription.end_date,
        },
    }
