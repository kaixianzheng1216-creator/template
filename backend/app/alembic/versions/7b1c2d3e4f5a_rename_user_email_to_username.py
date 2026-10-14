"""将用户邮箱字段重命名为用户名字段

Revision ID: 7b1c2d3e4f5a
Revises: fe56fa70289e
Create Date: 2026-10-14 00:00:00.000000

"""

from alembic import op


# Alembic 使用的迁移版本标识。
revision = "7b1c2d3e4f5a"
down_revision = "fe56fa70289e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_user_email", table_name="user")
    op.alter_column("user", "email", new_column_name="username")
    op.create_index("ix_user_username", "user", ["username"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_user_username", table_name="user")
    op.alter_column("user", "username", new_column_name="email")
    op.create_index("ix_user_email", "user", ["email"], unique=True)
