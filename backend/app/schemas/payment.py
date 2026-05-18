from typing import Optional

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    plan: str = "basic"


class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    plan: Optional[str] = "basic"
