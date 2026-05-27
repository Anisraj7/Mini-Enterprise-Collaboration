from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

from app.schemas.approval import (
    ApprovalOut,
)

from app.schemas.user import (
    UserOut,
)


# =====================================
# CREATE ESCALATION
# =====================================

class ApprovalEscalationCreate(
    BaseModel
):

    approval_id: int

    escalated_to: int

    reason: str = Field(
        ...,
        min_length=3,
        max_length=500,
    )


# =====================================
# ESCALATION RESPONSE
# =====================================

class ApprovalEscalationResponse(
    BaseModel
):

    id: int

    approval_id: int

    escalated_from: int

    escalated_to: int

    reason: str

    escalation_level: int

    status: str

    created_at: Optional[
        datetime
    ] = None

    resolved_at: Optional[
        datetime
    ] = None

    # =====================================
    # NESTED RELATIONSHIPS
    # =====================================

    approval: Optional[
        ApprovalOut
    ] = None

    escalated_from_user: Optional[
        UserOut
    ] = None

    escalated_to_user: Optional[
        UserOut
    ] = None

    # =====================================
    # PYDANTIC CONFIG
    # =====================================

    model_config = ConfigDict(
        from_attributes=True
    )