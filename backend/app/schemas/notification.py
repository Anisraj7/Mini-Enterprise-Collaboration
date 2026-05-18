from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# =========================================
# NOTIFICATION BASE
# =========================================
class NotificationBase(BaseModel):

    message: str


# =========================================
# CREATE NOTIFICATION
# =========================================
class NotificationCreate(NotificationBase):

    user_id: int

    organization_id: Optional[int] = None


# =========================================
# NOTIFICATION RESPONSE
# =========================================
class NotificationOut(NotificationBase):

    id: int

    user_id: int

    is_read: bool

    organization_id: Optional[int] = None

    created_at: datetime

    class Config:
        from_attributes = True