from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.channel import (
    ChannelCreate,
    ChannelUpdate,
    ChannelResponse
)

from app.services.channel_service import (
    ChannelService
)

from app.services.channel_member_service import (
    ChannelMemberService
)

from app.core.permissions import require_roles

from app.models.enums import UserRole

router = APIRouter()


@router.post(
    "",
    response_model=ChannelResponse
)
def create_channel(
    payload: ChannelCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value
            ]
        )
    )
):
    return ChannelService.create_channel(
        db,
        current_user,
        payload
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[ChannelResponse]
)
def list_channels(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value,
                UserRole.MEMBER.value,
                UserRole.VIEWER.value
            ]
        )
    )
):
    return ChannelService.get_channels(
        db,
        workspace_id,
        current_user
    )


@router.get(
    "/{channel_id}",
    response_model=ChannelResponse
)
def get_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value,
                UserRole.MEMBER.value,
                UserRole.VIEWER.value
            ]
        )
    )
):
    return ChannelService.get_channel(
        db,
        channel_id,
        current_user
    )


@router.put(
    "/{channel_id}",
    response_model=ChannelResponse
)
def update_channel(
    channel_id: int,
    payload: ChannelUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value
            ]
        )
    )
):
    return ChannelService.update_channel(
        db,
        channel_id,
        payload,
        current_user
    )


@router.patch(
    "/{channel_id}/archive",
    response_model=ChannelResponse
)
def archive_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value
            ]
        )
    )
):
    channel = ChannelService.get_channel(
        db,
        channel_id,
        current_user
    )
    return ChannelService.archive_channel(
        db,
        channel,
        current_user
    )


@router.patch(
    "/{channel_id}/restore",
    response_model=ChannelResponse
)
def restore_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value
            ]
        )
    )
):
    channel = ChannelService.get_channel(
        db,
        channel_id,
        current_user
    )
    return ChannelService.restore_channel(
        db,
        channel,
        current_user
    )


@router.post("/{channel_id}/join")
def join_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value,
                UserRole.MEMBER.value,
                UserRole.VIEWER.value
            ]
        )
    )
):
    return ChannelMemberService.join_channel(
        db,
        channel_id,
        current_user.id
    )


@router.post("/{channel_id}/leave")
def leave_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                UserRole.ORGANIZATION_ADMIN.value,
                UserRole.WORKSPACE_ADMIN.value,
                UserRole.MODERATOR.value,
                UserRole.MEMBER.value,
                UserRole.VIEWER.value
            ]
        )
    )
):
    return ChannelMemberService.leave_channel(
        db,
        channel_id,
        current_user.id
    )