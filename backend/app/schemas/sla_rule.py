from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SLARuleBase(BaseModel):
    module_name: str

    priority: str

    allowed_hours: int = Field(gt=0)

    escalation_enabled: bool = False

    escalation_after_hours: Optional[int] = None

    is_active: bool = True

    @field_validator("escalation_after_hours")
    @classmethod
    def validate_escalation_hours(
        cls,
        value,
    ):
        if value is not None and value <= 0:
            raise ValueError(
                "Escalation hours must be greater than 0"
            )
        return value


class SLARuleCreate(SLARuleBase):
    pass


class SLARuleUpdate(BaseModel):
    module_name: Optional[str] = None

    priority: Optional[str] = None

    allowed_hours: Optional[int] = None

    escalation_enabled: Optional[bool] = None

    escalation_after_hours: Optional[int] = None

    is_active: Optional[bool] = None


class SLARuleResponse(SLARuleBase):
    id: int

    created_by: int

    created_at: datetime

    updated_at: Optional[datetime]

    class Config:
        from_attributes = True