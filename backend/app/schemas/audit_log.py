from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# =========================================
# AUDIT RESPONSE
# =========================================
class AuditLogOut(BaseModel):

    id: int

    user_id: Optional[int]

    module_name: str

    action_type: str

    record_id: Optional[int]

    old_data: Optional[str]

    new_data: Optional[str]

    ip_address: Optional[str]

    user_agent: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True