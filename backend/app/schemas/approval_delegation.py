from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    field_validator,
    ConfigDict,
)


# =========================================
# BASE
# =========================================

class ApprovalDelegationBase(
    BaseModel
):

    delegatee_id: int

    start_date: datetime

    end_date: datetime

    reason: str

    @field_validator("end_date")
    @classmethod
    def validate_dates(
        cls,
        value,
        info,
    ):

        start_date = (
            info.data.get("start_date")
        )

        if (
            start_date
            and value <= start_date
        ):

            raise ValueError(
                "End date must be after start date"
            )

        return value


# =========================================
# CREATE
# =========================================

class ApprovalDelegationCreate(
    ApprovalDelegationBase
):
    pass


# =========================================
# RESPONSE
# =========================================

class ApprovalDelegationOut(
    ApprovalDelegationBase
):

    id: int

    delegator_id: int

    # =========================================
    # USER NAMES
    # =========================================

    delegator_name: Optional[
        str
    ] = None

    delegatee_name: Optional[
        str
    ] = None

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )