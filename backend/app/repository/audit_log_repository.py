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
            db.query(AuditLog)
            .order_by(
                AuditLog.id.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        audit_log_id: int,
    ):

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.id
                == audit_log_id
            )
            .first()
        )

    @staticmethod
    def get_by_module(
        db: Session,
        module_name: str,
    ):

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.module_name
                == module_name
            )
            .order_by(
                AuditLog.id.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.user_id
                == user_id
            )
            .order_by(
                AuditLog.id.desc()
            )
            .all()
        )