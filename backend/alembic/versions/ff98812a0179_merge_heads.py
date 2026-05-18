"""merge heads

Revision ID: ff98812a0179
Revises: 4b1d8183e03a, db_query_optimization
Create Date: 2026-05-13 19:50:38.819209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff98812a0179'
down_revision: Union[str, Sequence[str], None] = ('4b1d8183e03a', 'db_query_optimization')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
