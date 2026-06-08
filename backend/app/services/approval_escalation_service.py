from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.approval import Approval

from app.models.approval_escalation import (
    ApprovalEscalation,
)

from app.repository.approval_escalation_repository import (
    ApprovalEscalationRepository,
)


class ApprovalEscalationService:

    # =====================================
    # CREATE ESCALATION
    # =====================================
    @staticmethod
    def create_escalation(
        db: Session,
        approval_id: int,
        escalated_from: int,
        escalated_to: int,
        reason: str,
    ):
        """
        Create approval escalation
        """

        # VALIDATE APPROVAL

        approval = (
            db.execute(select(Approval).where(
                Approval.id == approval_id
            ))
            .scalars()
            .first()
        )

        if not approval:

            raise HTTPException(
                status_code=404,
                detail="Approval not found",
            )

        # PREVENT SELF ESCALATION

        if escalated_from == escalated_to:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Cannot escalate "
                    "to the same user"
                ),
            )

        # PREVENT DUPLICATE ACTIVE ESCALATION

        existing_escalation = (
            ApprovalEscalationRepository
            .existing_pending_escalation(
                db,
                approval_id,
            )
        )

        if existing_escalation:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Approval already has "
                    "a pending escalation"
                ),
            )

        # AUTO ESCALATION LEVEL

        latest_escalation = (
            ApprovalEscalationRepository
            .get_latest_by_approval_id(
                db,
                approval_id,
            )
        )

        escalation_level = (
            latest_escalation.escalation_level + 1
            if latest_escalation
            else 1
        )

        # CREATE ESCALATION

        escalation = ApprovalEscalation(
            approval_id=approval_id,
            escalated_from=escalated_from,
            escalated_to=escalated_to,
            reason=reason.strip(),
            escalation_level=escalation_level,
            status="PENDING",
            created_at=datetime.utcnow(),
        )

        created = (
            ApprovalEscalationRepository
            .create(
                db,
                escalation,
            )
        )

        # UPDATE APPROVAL

        approval.is_escalated = True

        approval.current_escalation_to = (
            escalated_to
        )

        approval.status = (
            "ESCALATED"
        )

        # UPDATE SLA STATUS

        if (
            approval.sla_status
            in [
                "ACTIVE",
                "BREACHED",
                "PENDING",
            ]
        ):
            approval.sla_status = (
                "ESCALATED"
            )

        db.commit()

        db.refresh(approval)

        db.refresh(created)

        return created

    # =====================================
    # GET ALL ESCALATIONS
    # =====================================
    @staticmethod
    def get_all_escalations(
        db: Session,
    ):
        """
        Get all escalations
        """

        return (
            ApprovalEscalationRepository
            .get_all(db)
        )

    # =====================================
    # GET PENDING ESCALATIONS
    # =====================================
    @staticmethod
    def get_pending_escalations(
        db: Session,
    ):
        """
        Get pending escalations
        """

        return (
            ApprovalEscalationRepository
            .get_pending(db)
        )

    # =====================================
    # GET ESCALATION HISTORY
    # =====================================
    @staticmethod
    def get_escalation_history(
        db: Session,
        approval_id: int,
    ):
        """
        Get escalation history
        """

        approval = (
            db.execute(select(Approval).where(
                Approval.id == approval_id
            ))
            .scalars()
            .first()
        )

        if not approval:

            raise HTTPException(
                status_code=404,
                detail="Approval not found",
            )

        return (
            ApprovalEscalationRepository
            .get_by_approval_id(
                db,
                approval_id,
            )
        )

    # =====================================
    # RESOLVE ESCALATION
    # =====================================
    @staticmethod
    def resolve_escalation(
        db: Session,
        escalation_id: int,
    ):
        """
        Resolve escalation
        """

        escalation = (
            ApprovalEscalationRepository
            .get_by_id(
                db,
                escalation_id,
            )
        )

        if not escalation:

            raise HTTPException(
                status_code=404,
                detail="Escalation not found",
            )

        if escalation.status == "RESOLVED":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Escalation already resolved"
                ),
            )

        if escalation.status == "CANCELLED":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Cancelled escalation "
                    "cannot be resolved"
                ),
            )

        # UPDATE ESCALATION

        escalation.status = "RESOLVED"

        escalation.resolved_at = (
            datetime.utcnow()
        )

        updated = (
            ApprovalEscalationRepository
            .update(
                db,
                escalation,
            )
        )

        # UPDATE APPROVAL

        approval = (
            db.execute(select(Approval).where(
                Approval.id
                == escalation.approval_id
            ))
            .scalars()
            .first()
        )

        if approval:

            approval.current_escalation_to = None

            approval.is_escalated = False

            approval.status = "APPROVED"

            if (
                approval.sla_status
                == "ESCALATED"
            ):
                approval.sla_status = (
                    "RESOLVED"
                )

            db.commit()

            db.refresh(approval)

            db.refresh(updated)

        return updated

    # =====================================
    # CANCEL ESCALATION
    # =====================================
    @staticmethod
    def cancel_escalation(
        db: Session,
        escalation_id: int,
    ):
        """
        Cancel escalation
        """

        escalation = (
            ApprovalEscalationRepository
            .get_by_id(
                db,
                escalation_id,
            )
        )

        if not escalation:

            raise HTTPException(
                status_code=404,
                detail="Escalation not found",
            )

        if escalation.status == "CANCELLED":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Escalation already cancelled"
                ),
            )

        if escalation.status == "RESOLVED":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Resolved escalation "
                    "cannot be cancelled"
                ),
            )

        # UPDATE ESCALATION

        escalation.status = "CANCELLED"

        updated = (
            ApprovalEscalationRepository
            .update(
                db,
                escalation,
            )
        )

        # UPDATE APPROVAL

        approval = (
            db.execute(select(Approval).where(
                Approval.id
                == escalation.approval_id
            ))
            .scalars()
            .first()
        )

        if approval:

            approval.current_escalation_to = None

            approval.is_escalated = False

            approval.status = "PENDING"

            if (
                approval.sla_status
                == "ESCALATED"
            ):
                approval.sla_status = (
                    "PENDING"
                )

            db.commit()

            db.refresh(approval)

            db.refresh(updated)

        return updated
