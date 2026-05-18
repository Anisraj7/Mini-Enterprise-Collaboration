from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ApprovalCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value


class ApprovalAction(BaseModel):
    action: str
    comment: Optional[str] = None

    @field_validator("action")
    @classmethod
    def validate_action(cls, value: str):
        normalized = value.strip().lower()
        if normalized not in {"approve", "reject", "hold"}:
            raise ValueError("Unsupported approval action")
        return normalized


class ApprovalOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    requested_by: int
    requested_by_name: Optional[str] = None
    status: str
    current_level: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApprovalHistoryOut(BaseModel):
    id: int
    approval_id: int
    action_by: int
    action_by_name: Optional[str] = None
    action: str
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
