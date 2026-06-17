from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.workspace_message import WorkspaceMessage


class WorkspaceMessageRepository:

    @staticmethod
    def create(
        db: Session,
        message: WorkspaceMessage,
    ) -> WorkspaceMessage:

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def get_by_id(
        db: Session,
        message_id: int,
    ) -> WorkspaceMessage | None:

        stmt = (
            select(WorkspaceMessage)
            .where(
                WorkspaceMessage.id == message_id
            )
        )

        result = db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def list_by_workspace(
        db: Session,
        workspace_id: int,
    ):

        stmt = (
            select(WorkspaceMessage)
            .where(
                WorkspaceMessage.workspace_id == workspace_id
            )
            .where(
                WorkspaceMessage.deleted_at.is_(None)
            )
            .order_by(
                WorkspaceMessage.created_at.desc()
            )
        )

        return paginate(
            db,
            stmt,
        )

    @staticmethod
    def update_content(
        db: Session,
        message: WorkspaceMessage,
        content: str,
    ) -> WorkspaceMessage:

        message.content = content
        message.edited_at = datetime.utcnow()

        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def soft_delete(
        db: Session,
        message: WorkspaceMessage,
    ) -> WorkspaceMessage:

        message.deleted_at = datetime.utcnow()

        db.commit()
        db.refresh(message)

        return message