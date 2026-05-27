from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =========================================
# NOTIFICATION BASE
# =========================================
class NotificationBase(BaseModel):

    title: Optional[str] = "System Notification"

    message: Optional[str] = ""

    notification_type: Optional[str] = "GENERAL"

    priority: Optional[str] = "MEDIUM"


# =========================================
# CREATE NOTIFICATION
# =========================================
class NotificationCreate(NotificationBase):

    user_id: int

    organization_id: Optional[int] = None


# =========================================
# UPDATE NOTIFICATION
# =========================================
class NotificationUpdate(BaseModel):

    is_read: Optional[bool] = None


# =========================================
# NOTIFICATION RESPONSE
# =========================================
class NotificationOut(NotificationBase):

    id: int

    user_id: int

    is_read: bool

    organization_id: Optional[int] = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )