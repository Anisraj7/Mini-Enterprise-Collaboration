from typing import cast

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.tenant_collab_settings import (
    TenantCollaborationSettings,
)
from app.models.tenant_collab_usage import (
    TenantCollaborationUsage,
)
from app.models.tenant_onboarding import (
    TenantOnboarding,
)

from app.repository.organization_repository import (
    OrganizationRepository,
)

from app.utils.slug import slugify


class OrganizationService:

    @staticmethod
    def create_organization(
        db: Session,
        data
    ):
        existing_name = (
            OrganizationRepository.get_by_name(
                db,
                data.name
            )
        )

        if existing_name:
            raise HTTPException(
                status_code=400,
                detail="Organization name already exists"
            )

        existing_email = (
            OrganizationRepository.get_by_email(
                db,
                data.contact_email
            )
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Organization email already exists"
            )

        slug = slugify(data.name)

        if (
            OrganizationRepository.get_by_slug(
                db,
                slug
            )
        ):
            raise HTTPException(
                status_code=400,
                detail="Organization slug already exists"
            )

        organization = Organization(
            name=data.name,
            slug=slug,
            contact_email=data.contact_email,
            phone=data.phone,
            address=data.address,
            industry=data.industry,
            plan=data.plan,
        )

        db.add(organization)
        db.flush()

        db.add(
            TenantCollaborationSettings(
                organization_id=organization.id
            )
        )

        db.add(
            TenantCollaborationUsage(
                organization_id=organization.id
            )
        )

        db.add(
            TenantOnboarding(
                organization_id=organization.id,
                onboarding_status="PENDING",
                settings_created=True,
                default_workspace_created=False,
            )
        )

        db.commit()
        db.refresh(organization)

        return organization

    @staticmethod
    def get_all(
        db: Session
    ):
        return OrganizationRepository.get_all(db)

    @staticmethod
    def get_organization(
        db: Session,
        organization_id: int
    ):
        organization = (
            OrganizationRepository.get_by_id(
                db,
                organization_id
            )
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        return organization

    @staticmethod
    def update_organization(
        db: Session,
        organization_id: int,
        data
    ):
        organization = (
            OrganizationRepository.get_by_id(
                db,
                organization_id
            )
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_name = (
                OrganizationRepository.get_by_name(
                    db,
                    update_data["name"]
                )
            )

            if isinstance(existing_name, Organization):
                existing_name_id = cast(int, existing_name.id)
                if existing_name_id != organization_id:
                    raise HTTPException(
                        status_code=400,
                        detail="Organization name already exists"
                    )

            new_slug = slugify(
                update_data["name"]
            )

            existing_slug = (
                OrganizationRepository.get_by_slug(
                    db,
                    new_slug
                )
            )

            if isinstance(existing_slug, Organization):
                existing_slug_id = cast(int, existing_slug.id)
                if existing_slug_id != organization_id:
                    raise HTTPException(
                        status_code=400,
                        detail="Organization slug already exists"
                    )

            setattr(organization, "slug", new_slug)

        if "contact_email" in update_data:
            existing_email = (
                OrganizationRepository.get_by_email(
                    db,
                    update_data["contact_email"]
                )
            )

            if isinstance(existing_email, Organization):
                existing_email_id = cast(int, existing_email.id)
                if existing_email_id != organization_id:
                    raise HTTPException(
                        status_code=400,
                        detail="Organization email already exists"
                    )

        for field, value in update_data.items():
            setattr(
                organization,
                field,
                value
            )

        return OrganizationRepository.update(
            db,
            organization
        )

    @staticmethod
    def suspend_organization(
        db: Session,
        organization_id: int
    ):
        organization = (
            OrganizationRepository.get_by_id(
                db,
                organization_id
            )
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        setattr(organization, "status", "ACTIVE")

        return OrganizationRepository.update(
            db,
            organization
        )

    @staticmethod
    def delete_organization(
        db: Session,
        organization_id: int
    ):
        organization = (
            OrganizationRepository.get_by_id(
                db,
                organization_id
            )
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        OrganizationRepository.delete(
            db,
            organization
        )

        return {
            "message": "Organization deleted"
        }
    @staticmethod
    def activate_organization(
        db: Session,
        organization_id: int
    ):
        organization = (
            OrganizationRepository.get_by_id(
                db,
                organization_id
            )
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        setattr(organization, "status", "ACTIVE")

        return OrganizationRepository.update(
            db,
            organization
        )