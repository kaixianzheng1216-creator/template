"""初始化数据库结构

迁移版本：a1b2c3d4e5f6
上一版本：
创建时间：2026-10-14 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "item",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("owner_id", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_item_owner_id", "item", ["owner_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_item_owner_id", table_name="item")
    op.drop_table("item")
