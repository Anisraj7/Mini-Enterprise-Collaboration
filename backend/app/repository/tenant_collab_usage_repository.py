from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tenant_collab_usage import (
    TenantCollaborationUsage,
)


class TenantCollaborationUsageRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        usage_id: int
    ) -> Optional[TenantCollaborationUsage]:
        return (
            db.execute(select(
                TenantCollaborationUsage
            )
            .where(
                TenantCollaborationUsage.id
                == usage_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_organization(
        db: Session,
        organization_id: int
    ) -> Optional[TenantCollaborationUsage]:
        return (
            db.execute(select(
                TenantCollaborationUsage
            )
            .where(
                TenantCollaborationUsage.organization_id
                == organization_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        usage: TenantCollaborationUsage
    ) -> TenantCollaborationUsage:
        db.commit()
        db.refresh(usage)
        return usage
