from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page

from app.db.database import get_db

from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.channel_message import (
    ChannelMessageCreate,
    ChannelMessageUpdate,
    ChannelMessageResponse,
)

from app.services.channel_message_service import (
    ChannelMessageService,
)

router = APIRouter(
    prefix="/channels",
    tags=["Channel Messages"],
)


@router.post(
    "/{channel_id}/messages",
    response_model=ChannelMessageResponse,
)
def create_channel_message(
    channel_id: int,
    payload: ChannelMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ChannelMessageService.create_message(
        db=db,
        organization_id=current_user.organization_id,
        workspace_id=0,
        channel_id=channel_id,
        sender_id=current_user.id,
        payload=payload,
    )


@router.get(
    "/{channel_id}/messages",
    response_model=Page[ChannelMessageResponse],
)
def list_channel_messages(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ChannelMessageService.list_messages(
        db=db,
        channel_id=channel_id,
    )