"""merge heads

Revision ID: 76be9e5e7b24
Revises: 0466e1dc54ce, migrate_user_roles
Create Date: 2026-06-03 19:46:44.615370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76be9e5e7b24'
down_revision: Union[str, Sequence[str], None] = ('0466e1dc54ce', 'migrate_user_roles')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
