from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.config import settings
from app.models import SQLModel

config = context.config

if config.config_file_name is None:
    raise RuntimeError("必须提供 Alembic 配置文件")

fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline():
    # 仅生成 SQL。
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # 连接数据库并执行迁移。
    connectable = create_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
