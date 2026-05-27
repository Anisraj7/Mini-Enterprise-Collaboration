from datetime import datetime

from sqlalchemy.orm import Session

from app.models.sla_tracking import (
    SLATracking,
)


class SLATrackingRepository:

    @staticmethod
    def create(
        db: Session,
        sla_tracking: SLATracking,
    ):
        """
        Create SLA tracking
        """

        db.add(sla_tracking)

        db.commit()

        db.refresh(sla_tracking)

        return sla_tracking

    @staticmethod
    def update(
        db: Session,
        sla_tracking: SLATracking,
    ):
        """
        Update SLA tracking
        """

        db.commit()

        db.refresh(sla_tracking)

        return sla_tracking

    @staticmethod
    def get_by_id(
        db: Session,
        tracking_id: int,
    ):
        """
        Get SLA tracking by ID
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.id
                == tracking_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
    ):
        """
        Get all SLA tracking records
        """

        return (
            db.query(SLATracking)
            .order_by(
                SLATracking.id.desc()
            )
            .all()
        )

    @staticmethod
    def get_active(
        db: Session,
    ):
        """
        Get active SLA records
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.status
                == "ACTIVE"
            )
            .order_by(
                SLATracking.due_time.asc()
            )
            .all()
        )

    @staticmethod
    def get_breached(
        db: Session,
    ):
        """
        Get breached SLA records
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.status
                == "BREACHED"
            )
            .order_by(
                SLATracking.due_time.desc()
            )
            .all()
        )

    @staticmethod
    def get_completed(
        db: Session,
    ):
        """
        Get completed SLA records
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.status.in_(
                    [
                        "COMPLETED_WITHIN_SLA",
                        "COMPLETED",
                    ]
                )
            )
            .order_by(
                SLATracking.completed_time.desc()
            )
            .all()
        )

    @staticmethod
    def get_escalated(
        db: Session,
    ):
        """
        Get escalated SLA records
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.status
                == "ESCALATED"
            )
            .order_by(
                SLATracking.updated_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_module(
        db: Session,
        module_name: str,
    ):
        """
        Get SLA tracking by module
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.module_name
                == module_name
            )
            .order_by(
                SLATracking.id.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_record(
        db: Session,
        module_name: str,
        record_id: int,
    ):
        """
        Get SLA tracking by module and record
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.module_name
                == module_name,
                SLATracking.record_id
                == record_id,
            )
            .order_by(
                SLATracking.id.desc()
            )
            .first()
        )

    @staticmethod
    def get_overdue_active(
        db: Session,
    ):
        """
        Get overdue active SLA records
        """

        current_time = datetime.utcnow()

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.status
                == "ACTIVE",
                SLATracking.due_time
                < current_time,
            )
            .order_by(
                SLATracking.due_time.asc()
            )
            .all()
        )

    @staticmethod
    def get_by_status(
        db: Session,
        status: str,
    ):
        """
        Get SLA records by status
        """

        return (
            db.query(SLATracking)
            .filter(
                SLATracking.status
                == status
            )
            .order_by(
                SLATracking.id.desc()
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        sla_tracking: SLATracking,
    ):
        """
        Delete SLA tracking
        """

        db.delete(sla_tracking)

        db.commit()

        return True