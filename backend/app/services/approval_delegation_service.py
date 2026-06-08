from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.approval_delegation import (
    ApprovalDelegation,
)

from app.models.user import User

from app.repository.approval_delegation_repository import (
    ApprovalDelegationRepository,
)

from app.schemas.approval_delegation import (
    ApprovalDelegationCreate,
)


class ApprovalDelegationService:

    @staticmethod
    def create_delegation(
        db: Session,
        user,
        payload: ApprovalDelegationCreate,
    ):

        existing_conflict = (
            ApprovalDelegationRepository.existing_conflict(
                db,
                user.id,
                payload.start_date,
                payload.end_date,
            )
        )

        if existing_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delegation date conflict exists",
            )

        delegation = ApprovalDelegation(
            delegator_id=user.id,
            delegatee_id=payload.delegatee_id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            reason=payload.reason,
        )

        delegation = (
            ApprovalDelegationRepository.create(
                db,
                delegation,
            )
        )

        delegator = (
            db.execute(select(User).where(User.id == delegation.delegator_id))
            .scalars()
            .first()
        )

        delegatee = (
            db.execute(select(User).where(User.id == delegation.delegatee_id))
            .scalars()
            .first()
        )

        delegation.delegator_name = (
            delegator.name
            if delegator
            else None
        )

        delegation.delegatee_name = (
            delegatee.name
            if delegatee
            else None
        )

        return delegation

    @staticmethod
    def get_my_delegations(
        db: Session,
        user,
    ):

        delegations = (
            ApprovalDelegationRepository.get_my_delegations(
                db,
                user.id,
            )
        )

        for delegation in delegations:

            delegator = (
                db.execute(select(User).where(User.id == delegation.delegator_id))
                .scalars()
                .first()
            )

            delegatee = (
                db.execute(select(User).where(User.id == delegation.delegatee_id))
                .scalars()
                .first()
            )

            delegation.delegator_name = (
                delegator.name
                if delegator
                else None
            )

            delegation.delegatee_name = (
                delegatee.name
                if delegatee
                else None
            )

        return delegations

    @staticmethod
    def get_active_delegations(
        db: Session,
    ):

        delegations = (
            ApprovalDelegationRepository.get_active(
                db
            )
        )

        for delegation in delegations:

            delegator = (
                db.execute(select(User).where(User.id == delegation.delegator_id))
                .scalars()
                .first()
            )

            delegatee = (
                db.execute(select(User).where(User.id == delegation.delegatee_id))
                .scalars()
                .first()
            )

            delegation.delegator_name = (
                delegator.name
                if delegator
                else None
            )

            delegation.delegatee_name = (
                delegatee.name
                if delegatee
                else None
            )

        return delegations

    @staticmethod
    def cancel_delegation(
        db: Session,
        delegation_id: int,
        user,
    ):

        delegation = (
            ApprovalDelegationRepository.get_by_id(
                db,
                delegation_id,
            )
        )

        if not delegation:
            raise HTTPException(
                status_code=404,
                detail="Delegation not found",
            )

        if delegation.delegator_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Not allowed",
            )

        delegation.is_active = False

        db.commit()

        db.refresh(delegation)

        delegator = (
            db.execute(select(User).where(User.id == delegation.delegator_id))
            .scalars()
            .first()
        )

        delegatee = (
            db.execute(select(User).where(User.id == delegation.delegatee_id))
            .scalars()
            .first()
        )

        delegation.delegator_name = (
            delegator.name
            if delegator
            else None
        )

        delegation.delegatee_name = (
            delegatee.name
            if delegatee
            else None
        )

        return delegation
