"""初始化数据库结构

Revision ID: 7b1c2d3e4f5a
Revises:
Create Date: 2026-10-14 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

revision = "7b1c2d3e4f5a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Uuid(), nullable=False),

        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),

        sa.Column("full_name", sa.String(length=255), nullable=True),

        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),

        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_user_username", "user", ["username"], unique=True)

    op.create_table(
        "item",
        sa.Column("id", sa.Uuid(), nullable=False),

        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),

        sa.Column("owner_id", sa.Uuid(), nullable=False),

        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),

        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("item")

    op.drop_index("ix_user_username", table_name="user")
    op.drop_table("user")
