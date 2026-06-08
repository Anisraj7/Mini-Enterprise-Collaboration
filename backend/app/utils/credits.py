from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select

from app.models.subscription import Subscription

def consume_credits(db, organization_id: int, amount: int):

    subscription = db.execute(select(Subscription).where(
        Subscription.organization_id == organization_id
    )).scalars().first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if subscription.status != "active":
        raise HTTPException(status_code=400, detail="Subscription is not active")

    if subscription.end_date and subscription.end_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Subscription has expired")

    if subscription.credits < amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient credits"
        )

    subscription.credits -= amount

    return subscription
