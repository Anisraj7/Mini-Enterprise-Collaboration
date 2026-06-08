from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import (
    AuditLog,
)


class AuditLogRepository:

    @staticmethod
    def create(
        db: Session,
        audit_log: AuditLog,
    ):

        db.add(audit_log)

        db.commit()

        db.refresh(audit_log)

        return audit_log

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.execute(select(AuditLog)
            .order_by(
                AuditLog.id.desc()
            ))
            .scalars()
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        audit_log_id: int,
    ):

        return (
            db.execute(select(AuditLog).where(
                AuditLog.id
                == audit_log_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_module(
        db: Session,
        module_name: str,
    ):

        return (
            db.execute(select(AuditLog).where(
                AuditLog.module_name
                == module_name
            )
            .order_by(
                AuditLog.id.desc()
            ))
            .scalars()
            .all()
        )

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
    ):

        return (
            db.execute(select(AuditLog).where(
                AuditLog.user_id
                == user_id
            )
            .order_by(
                AuditLog.id.desc()
            ))
            .scalars()
            .all()
        )
