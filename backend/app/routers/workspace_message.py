from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page

from app.db.database import get_db

from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.workspace_message import (
    WorkspaceMessageCreate,
    WorkspaceMessageUpdate,
    WorkspaceMessageResponse,
)

from app.services.workspace_message_service import (
    WorkspaceMessageService,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Messages"],
)


@router.post(
    "/{workspace_id}/messages",
    response_model=WorkspaceMessageResponse,
)
def create_workspace_message(
    workspace_id: int,
    payload: WorkspaceMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return WorkspaceMessageService.create_message(
        db=db,
        organization_id=current_user.organization_id,
        workspace_id=workspace_id,
        sender_id=current_user.id,
        payload=payload,
    )


@router.get(
    "/{workspace_id}/messages",
    response_model=Page[WorkspaceMessageResponse],
)
def list_workspace_messages(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return WorkspaceMessageService.list_messages(
        db=db,
        workspace_id=workspace_id,
    )