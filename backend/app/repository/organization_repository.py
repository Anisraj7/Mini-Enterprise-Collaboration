from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization import Organization


class OrganizationRepository:

    @staticmethod
    def create(
        db: Session,
        organization: Organization
    ) -> Organization:
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def get_by_id(
        db: Session,
        organization_id: int
    ) -> Optional[Organization]:
        return (
            db.execute(select(Organization).where(
                Organization.id == organization_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str
    ) -> Optional[Organization]:
        return (
            db.execute(select(Organization).where(
                Organization.name == name
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_slug(
        db: Session,
        slug: str
    ) -> Optional[Organization]:
        return (
            db.execute(select(Organization).where(
                Organization.slug == slug
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ) -> Optional[Organization]:
        return (
            db.execute(select(Organization).where(
                Organization.contact_email == email
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_all_stmt(
        db: Session
    ):
        return select(Organization).order_by(
            Organization.created_at.desc()
        )

    @staticmethod
    def get_all(db: Session) -> list[Organization]:
        return db.execute(
            OrganizationRepository.get_all_stmt(db)
        ).scalars().all()

    @staticmethod
    def update(
        db: Session,
        organization: Organization
    ) -> Organization:
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def delete(
        db: Session,
        organization: Organization
    ) -> None:
        db.delete(organization)
        db.commit()
