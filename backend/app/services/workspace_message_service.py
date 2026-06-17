from __future__ import annotations

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.models.workspace_message import WorkspaceMessage
from app.models.workspace_member import WorkspaceMember

from app.repository.workspace_message_repository import (
    WorkspaceMessageRepository,
)

from app.schemas.workspace_message import (
    WorkspaceMessageCreate,
    WorkspaceMessageUpdate,
)


class WorkspaceMessageService:

    @staticmethod
    def validate_workspace_member(
        workspace_member: WorkspaceMember | None,
    ) -> None:

        if workspace_member is None:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a workspace member",
            )

        if not workspace_member.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Workspace membership is inactive",
            )

    @staticmethod
    def validate_message_permission(
        message: WorkspaceMessage,
        workspace_member: WorkspaceMember,
        current_user_id: int,
    ) -> None:

        is_sender = (
            message.sender_id == current_user_id
        )

        is_workspace_admin = (
            workspace_member.role
            == "WORKSPACE_ADMIN"
        )

        if not (
            is_sender
            or is_workspace_admin
        ):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized",
            )

    @staticmethod
    def create_message(
        db: Session,
        organization_id: int,
        workspace_id: int,
        sender_id: int,
        payload: WorkspaceMessageCreate,
    ) -> WorkspaceMessage:

        message = WorkspaceMessage(
            organization_id=organization_id,
            workspace_id=workspace_id,
            sender_id=sender_id,
            content=payload.content,
        )

        return WorkspaceMessageRepository.create(
            db=db,
            message=message,
        )

    @staticmethod
    def get_message(
        db: Session,
        message_id: int,
    ) -> WorkspaceMessage | None:

        return WorkspaceMessageRepository.get_by_id(
            db=db,
            message_id=message_id,
        )

    @staticmethod
    def list_messages(
        db: Session,
        workspace_id: int,
    ):

        return WorkspaceMessageRepository.list_by_workspace(
            db=db,
            workspace_id=workspace_id,
        )

    @staticmethod
    def update_message(
        db: Session,
        message: WorkspaceMessage,
        payload: WorkspaceMessageUpdate,
    ) -> WorkspaceMessage:

        return WorkspaceMessageRepository.update_content(
            db=db,
            message=message,
            content=payload.content,
        )

    @staticmethod
    def delete_message(
        db: Session,
        message: WorkspaceMessage,
    ) -> WorkspaceMessage:

        return WorkspaceMessageRepository.soft_delete(
            db=db,
            message=message,
        )