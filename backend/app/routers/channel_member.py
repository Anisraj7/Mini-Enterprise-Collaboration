from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import (
    paginate,
)

from sqlalchemy.orm import Session

from app.core.permissions import (
    require_roles,
)

from app.db.database import get_db

from app.models.enums import (
    UserRole,
)

from app.schemas.channel_member import (
    ChannelMemberResponse,
)

from app.services.channel_member_service import (
    ChannelMemberService,
)

router = APIRouter()


allowed_roles = [
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.WORKSPACE_ADMIN.value,
    UserRole.MANAGER.value,
    UserRole.EMPLOYEE.value,
]


@router.get(
    "/{channel_id}/members",
    response_model=Page[ChannelMemberResponse],
)
def get_channel_members(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            allowed_roles
        )
    ),
):
    return paginate(
        db,
        ChannelMemberService.get_members_stmt(
            db,
            channel_id,
            current_user,
        ),
    )