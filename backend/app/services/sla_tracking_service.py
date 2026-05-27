from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sla_tracking import (
    SLATracking,
)
from app.models.approval import Approval
from app.models.task import Task
from app.models.sla_rule import SLARule

from app.repository.sla_tracking_repository import (
    SLATrackingRepository,
)


class SLATrackingService:

    @staticmethod
    def start_sla_tracking(
        db: Session,
        module_name: str,
        record_id: int,
        priority: str,
    ):
        """
        Start SLA tracking for task/approval
        """

        existing = (
            SLATrackingRepository.get_by_record(
                db,
                module_name,
                record_id,
            )
        )

        if (
            existing
            and not existing.completed_time
        ):
            return existing

        # FIND ACTIVE SLA RULE

        sla_rule = (
            db.query(SLARule)
            .filter(
                SLARule.module_name == module_name,
                SLARule.priority == priority,
                SLARule.is_active == True,
            )
            .first()
        )

        if not sla_rule:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No active SLA rule found"
                ),
            )

        # UTC NAIVE TIME
        start_time = datetime.utcnow()

        due_time = start_time + timedelta(
            hours=sla_rule.allowed_hours
        )

        sla_tracking = SLATracking(
            module_name=module_name,
            record_id=record_id,
            sla_rule_id=sla_rule.id,
            start_time=start_time,
            due_time=due_time,
            status="ACTIVE",
        )

        tracking = (
            SLATrackingRepository.create(
                db,
                sla_tracking,
            )
        )

        normalized_module = (
            module_name.lower()
        )

        # UPDATE TASK SLA

        if normalized_module == "task":

            task = (
                db.query(Task)
                .filter(
                    Task.id == record_id
                )
                .first()
            )

            if task:
                task.sla_status = (
                    tracking.status
                )

                task.sla_due_time = (
                    tracking.due_time
                )

                task.is_sla_breached = (
                    False
                )

                db.commit()

                db.refresh(task)

        # UPDATE APPROVAL SLA

        elif normalized_module == "approval":

            approval = (
                db.query(Approval)
                .filter(
                    Approval.id
                    == record_id
                )
                .first()
            )

            if approval:
                approval.sla_status = (
                    tracking.status
                )

                approval.sla_due_time = (
                    tracking.due_time
                )

                approval.is_escalated = (
                    False
                )

                db.commit()

                db.refresh(approval)

        return tracking

    @staticmethod
    def complete_sla(
        db: Session,
        tracking_id: int,
    ):
        """
        Complete SLA tracking
        """

        tracking = (
            SLATrackingRepository.get_by_id(
                db,
                tracking_id,
            )
        )

        if not tracking:
            raise HTTPException(
                status_code=404,
                detail=(
                    "SLA tracking not found"
                ),
            )

        if tracking.completed_time:
            raise HTTPException(
                status_code=400,
                detail=(
                    "SLA already completed"
                ),
            )

        # UTC NAIVE TIME
        completed_time = datetime.utcnow()

        # HANDLE TIMEZONE ISSUE
        due_time = tracking.due_time

        if (
            due_time
            and due_time.tzinfo
            is not None
        ):
            due_time = due_time.replace(
                tzinfo=None
            )

        if (
            completed_time.tzinfo
            is not None
        ):
            completed_time = (
                completed_time.replace(
                    tzinfo=None
                )
            )

        tracking.completed_time = (
            completed_time
        )

        # SLA STATUS CHECK

        if completed_time <= due_time:

            tracking.status = (
                "COMPLETED_WITHIN_SLA"
            )

            tracking.breach_reason = None

        else:

            tracking.status = "BREACHED"

            tracking.breach_reason = (
                "Completed after due time"
            )

        updated = (
            SLATrackingRepository.update(
                db,
                tracking,
            )
        )

        normalized_module = (
            tracking.module_name.lower()
        )

        # UPDATE TASK

        if normalized_module == "task":

            task = (
                db.query(Task)
                .filter(
                    Task.id
                    == tracking.record_id
                )
                .first()
            )

            if task:

                task.sla_status = (
                    tracking.status
                )

                task.sla_due_time = (
                    tracking.due_time
                )

                task.is_sla_breached = (
                    tracking.status
                    == "BREACHED"
                )

                db.commit()

                db.refresh(task)

        # UPDATE APPROVAL

        elif normalized_module == "approval":

            approval = (
                db.query(Approval)
                .filter(
                    Approval.id
                    == tracking.record_id
                )
                .first()
            )

            if approval:

                approval.sla_status = (
                    tracking.status
                )

                approval.sla_due_time = (
                    tracking.due_time
                )

                db.commit()

                db.refresh(approval)

        return updated

    @staticmethod
    def get_completed_sla(
        db: Session,
    ):
        """
        Get completed SLA records
        """

        return (
            SLATrackingRepository.get_completed(
                db
            )
        )

    @staticmethod
    def get_by_module(
        db: Session,
        module_name: str,
    ):
        """
        Get SLA records by module
        """

        return (
            SLATrackingRepository.get_by_module(
                db,
                module_name,
            )
        )

    @staticmethod
    def get_active_sla(
        db: Session,
    ):
        """
        Get active SLA records
        """

        return (
            SLATrackingRepository.get_active(
                db
            )
        )

    @staticmethod
    def get_breached_sla(
        db: Session,
    ):
        """
        Get breached SLA records
        """

        return (
            SLATrackingRepository.get_breached(
                db
            )
        )

    @staticmethod
    def get_sla_record(
        db: Session,
        module_name: str,
        record_id: int,
    ):
        """
        Get SLA record by module and record
        """

        tracking = (
            SLATrackingRepository.get_by_record(
                db,
                module_name,
                record_id,
            )
        )

        if not tracking:
            raise HTTPException(
                status_code=404,
                detail=(
                    "SLA record not found"
                ),
            )

        return tracking

    @staticmethod
    def get_overdue_active_slas(
        db: Session,
    ):
        """
        Get overdue active SLA records
        """

        current_time = datetime.utcnow()

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.status
                == "ACTIVE",
                SLATracking.due_time
                < current_time,
            )
            .all()
        )