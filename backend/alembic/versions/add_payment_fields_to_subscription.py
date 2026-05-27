"""add payment fields to subscription

Revision ID: add_payment_fields
Revises: ff98812a0179
Create Date: 2026-05-27 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "add_payment_fields"
down_revision: Union[str, Sequence[str], None] = "ff98812a0179"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_table(table_name: str) -> bool:
    return sa.inspect(op.get_bind()).has_table(table_name)


def _column_exists(table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    columns = [c["name"] for c in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    if _has_table("subscriptions"):
        if not _column_exists("subscriptions", "razorpay_order_id"):
            op.add_column(
                "subscriptions",
                sa.Column("razorpay_order_id", sa.String(), nullable=True),
            )

        if not _column_exists("subscriptions", "razorpay_payment_id"):
            op.add_column(
                "subscriptions",
                sa.Column("razorpay_payment_id", sa.String(), nullable=True),
            )

        if not _column_exists("subscriptions", "stripe_session_id"):
            op.add_column(
                "subscriptions",
                sa.Column("stripe_session_id", sa.String(), nullable=True),
            )

        if not _column_exists("subscriptions", "stripe_payment_intent_id"):
            op.add_column(
                "subscriptions",
                sa.Column("stripe_payment_intent_id", sa.String(), nullable=True),
            )


def downgrade() -> None:
    if _has_table("subscriptions"):
        if _column_exists("subscriptions", "razorpay_order_id"):
            op.drop_column("subscriptions", "razorpay_order_id")

        if _column_exists("subscriptions", "razorpay_payment_id"):
            op.drop_column("subscriptions", "razorpay_payment_id")

        if _column_exists("subscriptions", "stripe_session_id"):
            op.drop_column("subscriptions", "stripe_session_id")

        if _column_exists("subscriptions", "stripe_payment_intent_id"):
            op.drop_column("subscriptions", "stripe_payment_intent_id")
