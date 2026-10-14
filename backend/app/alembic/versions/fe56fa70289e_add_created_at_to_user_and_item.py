"""为用户和条目添加 created_at 字段

Revision ID: fe56fa70289e
Revises: 1a31ce608336
Create Date: 2026-01-23 15:50:37.171462

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# Alembic 使用的迁移版本标识。
revision = 'fe56fa70289e'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### 以下命令由 Alembic 自动生成，请按需调整！###
    op.add_column('item', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    # ### Alembic 命令结束 ###


def downgrade():
    # ### 以下命令由 Alembic 自动生成，请按需调整！###
    op.drop_column('user', 'created_at')
    op.drop_column('item', 'created_at')
    # ### Alembic 命令结束 ###
