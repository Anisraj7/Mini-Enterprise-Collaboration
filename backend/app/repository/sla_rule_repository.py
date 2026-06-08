from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from app.models.sla_rule import SLARule


class SLARuleRepository:

    @staticmethod
    def create(
        db: Session,
        sla_rule: SLARule,
    ):
        """
        Create SLA rule
        """

        db.add(sla_rule)

        db.commit()

        db.refresh(sla_rule)

        return sla_rule

    @staticmethod
    def get_all(
        db: Session,
    ):
        """
        Get all SLA rules
        """

        return (
            db.execute(select(SLARule)
            .order_by(
                SLARule.id.desc()
            ))
            .scalars()
            .all()
        )

    @staticmethod
    def get_active_rules(
        db: Session,
    ):
        """
        Get active SLA rules
        """

        return (
            db.execute(select(SLARule)
            .where(
                SLARule.is_active.is_(True)
            )
            .order_by(
                SLARule.id.desc()
            ))
            .scalars()
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        sla_rule_id: int,
    ):
        """
        Get SLA rule by ID
        """

        return (
            db.execute(select(SLARule).where(
                SLARule.id
                == sla_rule_id
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_module_and_priority(
        db: Session,
        module_name: str,
        priority: str,
    ):
        """
        Get SLA rule by module and priority
        """

        return (
            db.execute(
                select(SLARule).where(
                    and_(
                        func.lower(SLARule.module_name)
                        == module_name.lower(),

                        func.lower(SLARule.priority)
                        == priority.lower(),

                        SLARule.is_active.is_(True),
                    )
                )
            )
            .scalars()
            .first()
        )

    @staticmethod
    def get_active_by_module_and_priority(
        db: Session,
        module_name: str,
        priority: str,
    ):
        return (
            db.execute(
                select(SLARule).where(
                    and_(
                        func.lower(SLARule.module_name)
                        == module_name.lower(),

                        func.lower(SLARule.priority)
                        == priority.lower(),

                        SLARule.is_active.is_(True),
                    )
                )
            )
            .scalars()
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        sla_rule: SLARule,
    ):
        """
        Update SLA rule
        """

        db.commit()

        db.refresh(sla_rule)

        return sla_rule

    @staticmethod
    def delete(
        db: Session,
        sla_rule: SLARule,
    ):
        """
        Delete SLA rule
        """

        db.delete(sla_rule)

        db.commit()

        return True
