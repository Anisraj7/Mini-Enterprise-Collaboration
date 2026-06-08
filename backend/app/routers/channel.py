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

from app.schemas.channel import (
    ChannelCreate,
    ChannelUpdate,
    ChannelResponse,
)

from app.services.channel_service import (
    ChannelService,
)

from app.services.channel_member_service import (
    ChannelMemberService,
)

router = APIRouter()


read_roles = [
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.WORKSPACE_ADMIN.value,
    UserRole.MANAGER.value,
    UserRole.EMPLOYEE.value,
]

manage_roles = [
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.WORKSPACE_ADMIN.value,
    UserRole.MANAGER.value,
]


@router.post(
    "",
    response_model=ChannelResponse,
)
def create_channel(
    payload: ChannelCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return ChannelService.create_channel(
        db,
        current_user,
        payload,
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=Page[ChannelResponse],
)
def list_channels(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return paginate(
        db,
        ChannelService.get_channels_stmt(
            db,
            workspace_id,
            current_user,
        ),
    )


@router.get(
    "/{channel_id}",
    response_model=ChannelResponse,
)
def get_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return ChannelService.get_channel(
        db,
        channel_id,
        current_user,
    )


@router.put(
    "/{channel_id}",
    response_model=ChannelResponse,
)
def update_channel(
    channel_id: int,
    payload: ChannelUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return ChannelService.update_channel(
        db,
        channel_id,
        payload,
        current_user,
    )


@router.patch(
    "/{channel_id}/archive",
    response_model=ChannelResponse,
)
def archive_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return ChannelService.archive_channel(
        db,
        channel_id,
        current_user,
    )


@router.patch(
    "/{channel_id}/restore",
    response_model=ChannelResponse,
)
def restore_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return ChannelService.restore_channel(
        db,
        channel_id,
        current_user,
    )


@router.post(
    "/{channel_id}/join",
)
def join_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return ChannelMemberService.join_channel(
        db,
        channel_id,
        current_user.id,
    )


@router.post(
    "/{channel_id}/leave",
)
def leave_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return ChannelMemberService.leave_channel(
        db,
        channel_id,
        current_user.id,
    )