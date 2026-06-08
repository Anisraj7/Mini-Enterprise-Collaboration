from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tenant_collab_settings import (
    TenantCollaborationSettings,
)


class TenantCollaborationSettingsRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        settings_id: int
    ) -> Optional[TenantCollaborationSettings]:
        return (
            db.execute(select(
                TenantCollaborationSettings
            )
            .where(
                TenantCollaborationSettings.id
                == settings_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_organization(
        db: Session,
        organization_id: int
    ) -> Optional[TenantCollaborationSettings]:
        return (
            db.execute(select(
                TenantCollaborationSettings
            )
            .where(
                TenantCollaborationSettings.organization_id
                == organization_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        settings: TenantCollaborationSettings
    ) -> TenantCollaborationSettings:
        db.commit()
        db.refresh(settings)
        return settings
