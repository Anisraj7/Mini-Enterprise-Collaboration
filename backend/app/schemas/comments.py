from datetime import datetime
from typing import Optional

import bleach

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


# -----------------------------------
# COMMENT CREATE
# -----------------------------------
class CommentCreate(BaseModel):

    content: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

    is_internal: Optional[bool] = False


    # CONTENT VALIDATION
    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str):

        if not value.strip():

            raise ValueError(
                "Comment content cannot be empty"
            )

        return bleach.clean(value.strip())


# -----------------------------------
# COMMENT OUTPUT
# -----------------------------------
class CommentOut(BaseModel):

    id: int

    task_id: int

    user_id: int

    user_name: Optional[str] = None

    content: str

    is_internal: bool

    created_at: datetime


    class Config:
        from_attributes = True

