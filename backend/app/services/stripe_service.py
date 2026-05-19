import stripe

from fastapi import HTTPException

from app.core.config import (
    STRIPE_SECRET_KEY,
    STRIPE_PUBLISHABLE_KEY,
)

stripe.api_key = STRIPE_SECRET_KEY


PLAN_PRICES = {
    "basic": 499,
    "silver": 1499,
    "gold": 4999,
}


def create_checkout_session(plan: str):

    plan = plan.lower()

    if plan not in PLAN_PRICES:
        raise HTTPException(
            status_code=400,
            detail="Invalid plan"
        )

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
        }
    )

    return {
        "checkout_url": session.url,
        "public_key": STRIPE_PUBLISHABLE_KEY,
    }