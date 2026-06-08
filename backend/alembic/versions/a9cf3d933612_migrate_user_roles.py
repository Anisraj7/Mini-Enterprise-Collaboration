"""migrate user roles

Revision ID: migrate_user_roles
Revises: 117408341a94
Create Date: 2026-06-03

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "migrate_user_roles"
down_revision = "29b378dd4a26"
branch_labels = None
depends_on = None


def upgrade():

    conn = op.get_bind()

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'organization_admin'
            WHERE role = 'admin'
            """
        )
    )

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'workspace_admin'
            WHERE role = 'manager'
            """
        )
    )

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'member'
            WHERE role = 'employee'
            """
        )
    )

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'viewer'
            WHERE role = 'auditor'
            """
        )
    )

    # Set your platform account manually
    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'super_admin'
            WHERE email = 'YOUR_EMAIL_HERE'
            """
        )
    )


def downgrade():

    conn = op.get_bind()

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'admin'
            WHERE role = 'organization_admin'
            """
        )
    )

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'manager'
            WHERE role = 'workspace_admin'
            """
        )
    )

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'employee'
            WHERE role = 'member'
            """
        )
    )

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'auditor'
            WHERE role = 'viewer'
            """
        )
    )

    conn.execute(
        sa.text(
            """
            UPDATE users
            SET role = 'admin'
            WHERE role = 'super_admin'
            """
        )
    )