from datetime import datetime

from sqlalchemy.orm import (
    Session,
    aliased,
)

from app.models.approval_delegation import (
    ApprovalDelegation,
)

from app.models.user import User


class ApprovalDelegationRepository:

    @staticmethod
    def create(
        db: Session,
        delegation: ApprovalDelegation,
    ):

        db.add(delegation)

        db.commit()

        db.refresh(delegation)

        return delegation

    @staticmethod
    def get_my_delegations(
        db: Session,
        user_id: int,
    ):

        Delegator = aliased(User)

        Delegatee = aliased(User)

        results = (
            db.query(
                ApprovalDelegation,
                Delegator.name.label(
                    "delegator_name"
                ),
                Delegatee.name.label(
                    "delegatee_name"
                ),
            )
            .join(
                Delegator,
                ApprovalDelegation.delegator_id
                == Delegator.id,
            )
            .join(
                Delegatee,
                ApprovalDelegation.delegatee_id
                == Delegatee.id,
            )
            .filter(
                ApprovalDelegation.delegator_id
                == user_id
            )
            .order_by(
                ApprovalDelegation.id.desc()
            )
            .all()
        )

        delegations = []

        for (
            delegation,
            delegator_name,
            delegatee_name,
        ) in results:

            delegation.delegator_name = (
                delegator_name
            )

            delegation.delegatee_name = (
                delegatee_name
            )

            delegations.append(
                delegation
            )

        return delegations

    @staticmethod
    def get_active(
        db: Session,
    ):

        now = datetime.utcnow()

        Delegator = aliased(User)

        Delegatee = aliased(User)

        results = (
            db.query(
                ApprovalDelegation,
                Delegator.name.label(
                    "delegator_name"
                ),
                Delegatee.name.label(
                    "delegatee_name"
                ),
            )
            .join(
                Delegator,
                ApprovalDelegation.delegator_id
                == Delegator.id,
            )
            .join(
                Delegatee,
                ApprovalDelegation.delegatee_id
                == Delegatee.id,
            )
            .filter(
                ApprovalDelegation.is_active
                == True,
                ApprovalDelegation.start_date
                <= now,
                ApprovalDelegation.end_date
                >= now,
            )
            .all()
        )

        delegations = []

        for (
            delegation,
            delegator_name,
            delegatee_name,
        ) in results:

            delegation.delegator_name = (
                delegator_name
            )

            delegation.delegatee_name = (
                delegatee_name
            )

            delegations.append(
                delegation
            )

        return delegations

    @staticmethod
    def get_by_id(
        db: Session,
        delegation_id: int,
    ):

        return (
            db.query(
                ApprovalDelegation
            )
            .filter(
                ApprovalDelegation.id
                == delegation_id
            )
            .first()
        )

    @staticmethod
    def existing_conflict(
        db: Session,
        delegator_id: int,
        start_date,
        end_date,
    ):

        return (
            db.query(
                ApprovalDelegation
            )
            .filter(
                ApprovalDelegation.delegator_id
                == delegator_id,
                ApprovalDelegation.is_active
                == True,
                ApprovalDelegation.start_date
                <= end_date,
                ApprovalDelegation.end_date
                >= start_date,
            )
            .first()
        )