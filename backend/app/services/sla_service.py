from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sla_rule import SLARule

from app.repository.sla_rule_repository import (
    SLARuleRepository,
)

from app.schemas.sla_rule import (
    SLARuleCreate,
    SLARuleUpdate,
)


class SLARuleService:

    @staticmethod
    def create_sla_rule(
        db: Session,
        payload: SLARuleCreate,
        user_id: int,
    ):
        """
        Create SLA Rule
        """

        # VALIDATION

        if payload.allowed_hours <= 0:
            raise HTTPException(
                status_code=400,
                detail="Allowed hours must be greater than 0",
            )

        if (
            payload.escalation_enabled
            and payload.escalation_after_hours is not None
            and payload.escalation_after_hours <= 0
        ):
            raise HTTPException(
                status_code=400,
                detail="Escalation after hours must be greater than 0",
            )

        if (
            payload.escalation_enabled
            and payload.escalation_after_hours
            and payload.escalation_after_hours
            >= payload.allowed_hours
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Escalation hours must be less "
                    "than allowed hours"
                ),
            )

        # CHECK DUPLICATE ACTIVE RULE

        existing_rule = (
            SLARuleRepository.get_by_module_and_priority(
                db,
                payload.module_name,
                payload.priority,
            )
        )

        if existing_rule:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Active SLA rule already exists "
                    "for this module and priority"
                ),
            )

        # CREATE SLA RULE

        sla_rule = SLARule(
            module_name=payload.module_name,
            priority=payload.priority,
            allowed_hours=payload.allowed_hours,
            escalation_enabled=payload.escalation_enabled,
            escalation_after_hours=payload.escalation_after_hours,
            is_active=payload.is_active,
            created_by=user_id,
        )

        return SLARuleRepository.create(
            db,
            sla_rule,
        )

    @staticmethod
    def get_all_sla_rules(
        db: Session,
    ):
        """
        Get all SLA rules
        """

        return SLARuleRepository.get_all(db)

    @staticmethod
    def get_active_sla_rules(
        db: Session,
    ):
        """
        Get active SLA rules
        """

        return SLARuleRepository.get_active_rules(
            db,
        )

    @staticmethod
    def get_sla_rule_by_id(
        db: Session,
        sla_rule_id: int,
    ):
        """
        Get SLA rule by ID
        """

        sla_rule = SLARuleRepository.get_by_id(
            db,
            sla_rule_id,
        )

        if not sla_rule:
            raise HTTPException(
                status_code=404,
                detail="SLA rule not found",
            )

        return sla_rule

    @staticmethod
    def update_sla_rule(
        db: Session,
        sla_rule_id: int,
        payload: SLARuleUpdate,
    ):
        """
        Update SLA rule
        """

        sla_rule = (
            SLARuleService.get_sla_rule_by_id(
                db,
                sla_rule_id,
            )
        )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        # VALIDATIONS

        allowed_hours = update_data.get(
            "allowed_hours",
            sla_rule.allowed_hours,
        )

        escalation_enabled = update_data.get(
            "escalation_enabled",
            sla_rule.escalation_enabled,
        )

        escalation_after_hours = update_data.get(
            "escalation_after_hours",
            sla_rule.escalation_after_hours,
        )

        if allowed_hours <= 0:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Allowed hours must be "
                    "greater than 0"
                ),
            )

        if (
            escalation_enabled
            and escalation_after_hours is not None
            and escalation_after_hours <= 0
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Escalation after hours must "
                    "be greater than 0"
                ),
            )

        if (
            escalation_enabled
            and escalation_after_hours
            and escalation_after_hours
            >= allowed_hours
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Escalation hours must be "
                    "less than allowed hours"
                ),
            )

        # UPDATE FIELDS

        for key, value in update_data.items():
            setattr(
                sla_rule,
                key,
                value,
            )

        return SLARuleRepository.update(
            db,
            sla_rule,
        )

    @staticmethod
    def disable_sla_rule(
        db: Session,
        sla_rule_id: int,
    ):
        """
        Disable SLA rule
        """

        sla_rule = (
            SLARuleService.get_sla_rule_by_id(
                db,
                sla_rule_id,
            )
        )

        if not sla_rule.is_active:
            raise HTTPException(
                status_code=400,
                detail="SLA rule already disabled",
            )

        sla_rule.is_active = False

        return SLARuleRepository.update(
            db,
            sla_rule,
        )

    @staticmethod
    def get_matching_sla_rule(
        db: Session,
        module_name: str,
        priority: str,
    ):
        """
        Get matching active SLA rule
        for task/approval creation
        """

        sla_rule = (
            SLARuleRepository.get_active_by_module_and_priority(
                db,
                module_name,
                priority,
            )
        )

        if not sla_rule:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No active SLA rule found "
                    "for this module and priority"
                ),
            )

        return sla_rule