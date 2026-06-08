from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password

from app.models.organization import Organization
from app.models.enums import UserRole
from app.models.tenant_collab_settings import (
    TenantCollaborationSettings,
)
from app.models.tenant_collab_usage import (
    TenantCollaborationUsage,
)
from app.models.tenant_onboarding import (
    TenantOnboarding,
)
from app.models.user import User
from app.models.workspace import Workspace

from app.utils.slug import slugify


class TenantOnboardingService:

    @staticmethod
    def onboard_tenant(
        db: Session,
        payload
    ):
        try:
            org_slug = slugify(
                payload.organization_name
            )

            if db.execute(select(Organization).where(
                Organization.name
                == payload.organization_name
            )).scalars().first():
                raise HTTPException(
                    status_code=409,
                    detail="Organization already exists"
                )

            if db.execute(select(Organization).where(
                Organization.slug == org_slug
            )).scalars().first():
                raise HTTPException(
                    status_code=409,
                    detail="Organization slug already exists"
                )

            if db.execute(select(Organization).where(
                Organization.contact_email
                == payload.organization_email
            )).scalars().first():
                raise HTTPException(
                    status_code=409,
                    detail="Organization email already exists"
                )

            if db.execute(select(User).where(
                User.email == payload.admin_email
            )).scalars().first():
                raise HTTPException(
                    status_code=409,
                    detail="Admin email already exists"
                )

            organization = Organization(
                name=payload.organization_name,
                slug=org_slug,
                contact_email=payload.organization_email,
                status="ACTIVE"
            )

            db.add(organization)
            db.flush()

            admin_user = User(
                name=payload.admin_name,
                email=payload.admin_email,
                hashed_password=hash_password(
                    payload.password
                ),
                role=UserRole.ORGANIZATION_ADMIN.value,
                organization_id=organization.id
            )

            db.add(admin_user)
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

            workspace_created = False

            if payload.create_default_workspace:
                workspace = Workspace(
                    organization_id=organization.id,
                    name="General",
                    slug=f"general-{organization.id}",
                    visibility="PUBLIC",
                    created_by=admin_user.id
                )

                db.add(workspace)
                workspace_created = True

            onboarding = TenantOnboarding(
                organization_id=organization.id,
                admin_user_id=admin_user.id,
                onboarding_status="COMPLETED",
                settings_created=True,
                default_workspace_created=workspace_created,
                completed_at=datetime.utcnow()
            )

            db.add(onboarding)

            db.commit()
            db.refresh(onboarding)

            return onboarding

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Tenant onboarding failed"
            )

    @staticmethod
    def create_admin(
        db: Session,
        organization_id: int,
        payload
    ):
        try:
            organization = db.execute(select(
                Organization
            ).where(
                Organization.id == organization_id
            )).scalars().first()

            if not organization:
                raise HTTPException(
                    status_code=404,
                    detail="Organization not found"
                )

            existing_org_admin = db.execute(select(
                User
            ).where(
                User.organization_id
                == organization_id,
                User.role
                == UserRole.ORGANIZATION_ADMIN.value
            )).scalars().first()

            if existing_org_admin:
                raise HTTPException(
                    status_code=409,
                    detail="Organization admin already exists"
                )

            if db.execute(select(User).where(
                User.email == payload.email
            )).scalars().first():
                raise HTTPException(
                    status_code=409,
                    detail="Admin email already exists"
                )

            admin_user = User(
                name=payload.name,
                email=payload.email,
                hashed_password=hash_password(
                    payload.password
                ),
                role=UserRole.ORGANIZATION_ADMIN.value,
                organization_id=organization.id
            )

            db.add(admin_user)
            db.flush()

            onboarding = db.execute(select(
                TenantOnboarding
            ).where(
                TenantOnboarding.organization_id
                == organization.id
            )).scalars().first()

            if not onboarding:
                onboarding = TenantOnboarding(
                    organization_id=organization.id
                )
                db.add(onboarding)

            onboarding.admin_user_id = admin_user.id
            onboarding.settings_created = True
            onboarding.onboarding_status = (
                "COMPLETED"
            )
            onboarding.completed_at = (
                datetime.utcnow()
            )

            db.commit()
            db.refresh(onboarding)

            return onboarding

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Admin creation failed"
            )

    @staticmethod
    def get_status(
        db: Session,
        organization_id: int
    ):
        onboarding = db.execute(select(
            TenantOnboarding
        ).where(
            TenantOnboarding.organization_id
            == organization_id
        ).order_by(
            TenantOnboarding.created_at.desc()
        )).scalars().first()

        if not onboarding:
            raise HTTPException(
                status_code=404,
                detail="Onboarding record not found"
            )

        return onboarding
