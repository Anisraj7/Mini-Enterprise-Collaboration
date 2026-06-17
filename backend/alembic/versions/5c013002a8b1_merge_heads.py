"""merge heads

Revision ID: 5c013002a8b1
Revises: 1f2e3d4c5b6a, 47d758b0e2cb, 76be9e5e7b24, add_payment_fields
Create Date: 2026-06-10 16:38:14.662752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c013002a8b1'
down_revision: Union[str, Sequence[str], None] = ('1f2e3d4c5b6a', '47d758b0e2cb', '76be9e5e7b24', 'add_payment_fields')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
    "channel_members",
    sa.Column(
        "role",
        sa.String(length=30),
        nullable=True,
    ),
    )

    op.execute(
        """
        UPDATE channel_members
        SET role = 'MEMBER'
        WHERE role IS NULL
        """
    )

    op.alter_column(
        "channel_members",
        "role",
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
