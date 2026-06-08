from alembic import op


revision = "make_first_user_super_admin"
down_revision = "29b378dd4a26"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE users
        SET role = 'super_admin'
        WHERE email = 'anis@super.com'
    """)


def downgrade():
    op.execute("""
        UPDATE users
        SET role = 'admin'
        WHERE email = 'anis@super.com'
    """)