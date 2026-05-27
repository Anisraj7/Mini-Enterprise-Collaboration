from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.models.approval_escalation import (
    ApprovalEscalation,
)


class ApprovalEscalationRepository:

    @staticmethod
    def create(
        db: Session,
        escalation: ApprovalEscalation,
    ):
        db.add(escalation)

        db.commit()

        db.refresh(escalation)

        return escalation

    @staticmethod
    def update(
        db: Session,
        escalation: ApprovalEscalation,
    ):
        db.commit()

        db.refresh(escalation)

        return escalation

    @staticmethod
    def get_by_id(
        db: Session,
        escalation_id: int,
    ):
        return (
            db.query(ApprovalEscalation)
            .options(
                joinedload(
                    ApprovalEscalation.approval
                ),
                joinedload(
                    ApprovalEscalation.escalated_from_user
                ),
                joinedload(
                    ApprovalEscalation.escalated_to_user
                ),
            )
            .filter(
                ApprovalEscalation.id
                == escalation_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
    ):
        return (
            db.query(ApprovalEscalation)
            .options(
                joinedload(
                    ApprovalEscalation.approval
                ),
                joinedload(
                    ApprovalEscalation.escalated_from_user
                ),
                joinedload(
                    ApprovalEscalation.escalated_to_user
                ),
            )
            .order_by(
                ApprovalEscalation.id.desc()
            )
            .all()
        )

    @staticmethod
    def get_pending(
        db: Session,
    ):
        return (
            db.query(ApprovalEscalation)
            .options(
                joinedload(
                    ApprovalEscalation.approval
                ),
                joinedload(
                    ApprovalEscalation.escalated_from_user
                ),
                joinedload(
                    ApprovalEscalation.escalated_to_user
                ),
            )
            .filter(
                ApprovalEscalation.status
                == "PENDING"
            )
            .order_by(
                ApprovalEscalation.id.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_approval_id(
        db: Session,
        approval_id: int,
    ):
        return (
            db.query(ApprovalEscalation)
            .options(
                joinedload(
                    ApprovalEscalation.approval
                ),
                joinedload(
                    ApprovalEscalation.escalated_from_user
                ),
                joinedload(
                    ApprovalEscalation.escalated_to_user
                ),
            )
            .filter(
                ApprovalEscalation.approval_id
                == approval_id
            )
            .order_by(
                ApprovalEscalation.id.desc()
            )
            .all()
        )

    @staticmethod
    def existing_pending_escalation(
        db: Session,
        approval_id: int,
    ):
        return (
            db.query(ApprovalEscalation)
            .options(
                joinedload(
                    ApprovalEscalation.approval
                ),
                joinedload(
                    ApprovalEscalation.escalated_from_user
                ),
                joinedload(
                    ApprovalEscalation.escalated_to_user
                ),
            )
            .filter(
                ApprovalEscalation.approval_id
                == approval_id,
                ApprovalEscalation.status
                == "PENDING",
            )
            .first()
        )

    @staticmethod
    def get_latest_by_approval_id(
        db: Session,
        approval_id: int,
    ):
        return (
            db.query(ApprovalEscalation)
            .options(
                joinedload(
                    ApprovalEscalation.approval
                ),
                joinedload(
                    ApprovalEscalation.escalated_from_user
                ),
                joinedload(
                    ApprovalEscalation.escalated_to_user
                ),
            )
            .filter(
                ApprovalEscalation.approval_id
                == approval_id
            )
            .order_by(
                ApprovalEscalation.id.desc()
            )
            .first()
        )