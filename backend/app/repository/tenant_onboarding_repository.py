from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tenant_onboarding import (
    TenantOnboarding,
)


class TenantOnboardingRepository:

    @staticmethod
    def create(
        db: Session,
        onboarding: TenantOnboarding
    ) -> TenantOnboarding:
        db.add(onboarding)
        db.commit()
        db.refresh(onboarding)
        return onboarding

    @staticmethod
    def get_by_id(
        db: Session,
        onboarding_id: int
    ) -> Optional[TenantOnboarding]:
        return (
            db.execute(select(TenantOnboarding).where(
                TenantOnboarding.id == onboarding_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_organization(
        db: Session,
        organization_id: int
    ) -> Optional[TenantOnboarding]:
        return (
            db.execute(select(TenantOnboarding).where(
                TenantOnboarding.organization_id
                == organization_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        onboarding: TenantOnboarding
    ) -> TenantOnboarding:
        db.commit()
        db.refresh(onboarding)
        return onboarding
