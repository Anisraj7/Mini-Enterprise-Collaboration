import logging

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


logger = logging.getLogger("mini_enterprise.schema")


def _type_sql(dialect: str, kind: str) -> str:
    if kind == "bool":
        return "BOOLEAN DEFAULT FALSE"

    if kind == "datetime":
        return "TIMESTAMP NULL"

    if kind == "int":
        return "INTEGER NULL"

    if kind == "text":
        return "TEXT NULL"

    if kind.startswith("string:"):
        return f"VARCHAR({kind.split(':', 1)[1]}) NULL"

    return "VARCHAR(255) NULL"


def _add_missing_columns(
    engine: Engine,
    table_name: str,
    columns: dict[str, str],
) -> None:
    inspector = inspect(engine)

    if not inspector.has_table(table_name):
        return

    existing = {
        column["name"]
        for column in inspector.get_columns(table_name)
    }

    missing = {
        name: kind
        for name, kind in columns.items()
        if name not in existing
    }

    if not missing:
        return

    dialect = engine.dialect.name

    with engine.begin() as connection:
        for name, kind in missing.items():
            ddl = (
                f"ALTER TABLE {table_name} "
                f"ADD COLUMN {name} {_type_sql(dialect, kind)}"
            )
            connection.execute(text(ddl))
            logger.info(
                "Added missing column %s.%s",
                table_name,
                name,
            )


def ensure_phase9_schema(engine: Engine) -> None:
    """Patch older dev databases that were created before Phase 9 columns."""

    _add_missing_columns(
        engine,
        "notifications",
        {
            "title": "string:255",
            "notification_type": "string:100",
            "priority": "string:50",
        },
    )

    _add_missing_columns(
        engine,
        "tasks",
        {
            "sla_status": "string:50",
            "sla_due_time": "datetime",
            "is_sla_breached": "bool",
        },
    )

    _add_missing_columns(
        engine,
        "approvals",
        {
            "sla_status": "string:50",
            "sla_due_time": "datetime",
            "is_escalated": "bool",
            "current_escalation_to": "int",
        },
    )

    _add_missing_columns(
        engine,
        "audit_logs",
        {
            "organization_id": "int",
            "module_name": "string:255",
            "action_type": "string:255",
            "record_id": "int",
            "old_data": "text",
            "new_data": "text",
            "ip_address": "string:255",
            "user_agent": "text",
            "created_at": "datetime",
        },
    )
