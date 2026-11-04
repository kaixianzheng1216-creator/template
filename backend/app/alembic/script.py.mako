"""${message}

迁移版本：${up_revision}
上一版本：${down_revision | comma,n}
创建时间：${create_date}

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op
${imports if imports else ""}

# Alembic 使用的迁移版本标识。
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
