"""empty message

Revision ID: 3e2ac2fe7025
Revises: 9797e8933cdc
Create Date: 2026-06-15 21:33:23.635370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e2ac2fe7025'
down_revision: Union[str, Sequence[str], None] = "5c013002a8b1"
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
