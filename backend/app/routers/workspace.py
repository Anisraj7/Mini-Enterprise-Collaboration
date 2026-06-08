from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import (
    Page,
    paginate,
)

from fastapi_pagination.ext.sqlalchemy import (
    paginate as paginate_sqlalchemy,
)

from sqlalchemy.orm import Session

from app.core.permissions import require_roles

from app.db.database import get_db

from app.models.enums import UserRole

from app.schemas.channel import ChannelResponse

from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceUpdate,
)

from app.services.channel_service import (
    ChannelService,
)

from app.services.workspace_service import (
    WorkspaceService,
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
]


@router.post(
    "",
    response_model=WorkspaceResponse,
)
def create_workspace(
    payload: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return WorkspaceService.create_workspace(
        db,
        current_user,
        payload,
    )


@router.get(
    "",
    response_model=Page[WorkspaceResponse],
)
def list_workspaces(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return paginate_sqlalchemy(
        db,
        WorkspaceService.get_workspaces_stmt(
            db,
            current_user,
        ),
    )


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return WorkspaceService.get_workspace(
        db,
        workspace_id,
        current_user,
    )


@router.put(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def update_workspace(
    workspace_id: int,
    payload: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return WorkspaceService.update_workspace(
        db,
        workspace_id,
        payload,
        current_user,
    )


@router.patch(
    "/{workspace_id}/archive",
    response_model=WorkspaceResponse,
)
def archive_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return WorkspaceService.archive_workspace(
        db,
        workspace_id,
        current_user,
    )


@router.patch(
    "/{workspace_id}/restore",
    response_model=WorkspaceResponse,
)
def restore_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return WorkspaceService.restore_workspace(
        db,
        workspace_id,
        current_user,
    )


@router.get(
    "/{workspace_id}/channels",
    response_model=Page[ChannelResponse],
)
def list_workspace_channels(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return paginate_sqlalchemy(
        db,
        ChannelService.get_channels_stmt(
            db,
            workspace_id,
            current_user,
        ),
    )