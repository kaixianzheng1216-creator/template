"""添加级联删除关系

Revision ID: 1a31ce608336
Revises: d98dd8ec85a3
Create Date: 2024-07-31 22:24:34.447891

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# Alembic 使用的迁移版本标识。
revision = '1a31ce608336'
down_revision = 'd98dd8ec85a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### 以下命令由 Alembic 自动生成，请按需调整！###
    op.alter_column('item', 'owner_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('item_owner_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key(None, 'item', 'user', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### Alembic 命令结束 ###


def downgrade():
    # ### 以下命令由 Alembic 自动生成，请按需调整！###
    op.drop_constraint('item_owner_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key('item_owner_id_fkey', 'item', 'user', ['owner_id'], ['id'])
    op.alter_column('item', 'owner_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### Alembic 命令结束 ###
