import json

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.audit_log import (
    AuditLog,
)

from app.repository.audit_log_repository import (
    AuditLogRepository,
)


class AuditLogService:

    @staticmethod
    def create_audit_log(
        db: Session,
        user_id: int | None,
        module_name: str,
        action_type: str,
        record_id: int | None = None,
        old_data=None,
        new_data=None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ):

        audit_log = AuditLog(
            user_id=user_id,
            module_name=module_name,
            action_type=action_type,
            record_id=record_id,
            old_data=json.dumps(old_data)
            if old_data
            else None,
            new_data=json.dumps(new_data)
            if new_data
            else None,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return (
            AuditLogRepository.create(
                db,
                audit_log,
            )
        )

    @staticmethod
    def get_all_logs(
        db: Session,
    ):
        return (
            AuditLogRepository.get_all(db)
        )

    @staticmethod
    def get_log_by_id(
        db: Session,
        audit_log_id: int,
    ):

        log = (
            AuditLogRepository.get_by_id(
                db,
                audit_log_id,
            )
        )

        if not log:
            raise HTTPException(
                status_code=404,
                detail="Audit log not found",
            )

        return log

    @staticmethod
    def get_logs_by_module(
        db: Session,
        module_name: str,
    ):
        return (
            AuditLogRepository.get_by_module(
                db,
                module_name,
            )
        )

    @staticmethod
    def get_logs_by_user(
        db: Session,
        user_id: int,
    ):
        return (
            AuditLogRepository.get_by_user(
                db,
                user_id,
            )
        )