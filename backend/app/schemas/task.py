from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import bleach

from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


def validate_future_due_date(value: Optional[datetime]):
    if value:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        if value < datetime.now(timezone.utc):
            raise ValueError("Due date cannot be in the past")

    return value


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

    description: Optional[str] = Field(None, max_length=1000)

    status: TaskStatus = TaskStatus.todo

    priority: TaskPriority = TaskPriority.medium

    due_date: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("Title cannot be empty")

        return bleach.clean(value.strip())

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value:
            return bleach.clean(value.strip())

        return value


class TaskCreate(TaskBase):
    assigned_to_id: Optional[int] = None

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value):
        return validate_future_due_date(value)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)

    description: Optional[str] = Field(None, max_length=1000)

    status: Optional[TaskStatus] = None

    priority: Optional[TaskPriority] = None

    due_date: Optional[datetime] = None

    assigned_to_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is not None:
            if not value.strip():
                raise ValueError("Title cannot be empty")

            return bleach.clean(value.strip())

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value:
            return bleach.clean(value.strip())

        return value

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value):
        return validate_future_due_date(value)


class TaskAssign(BaseModel):
    assigned_to_id: int


class TaskOut(TaskBase):
    id: int

    created_by_id: int

    assigned_to_id: Optional[int]

    assigned_to_name: Optional[str] = None

    updated_by: Optional[int] = None

    document: Optional[str] = None

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


class TaskStatusUpdate(BaseModel):
    status: TaskStatus