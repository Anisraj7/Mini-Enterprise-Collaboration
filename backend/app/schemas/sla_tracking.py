from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SLATrackingResponse(BaseModel):
    id: int

    module_name: str

    record_id: int

    sla_rule_id: int

    start_time: datetime

    due_time: datetime

    completed_time: Optional[datetime]

    status: str

    breach_reason: Optional[str]

    class Config:
        from_attributes = True