from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Alembic 配置对象，用于读取当前 .ini 文件中的配置值。
config = context.config

# 读取配置文件并初始化 Python 日志记录器。
assert config.config_file_name is not None
fileConfig(config.config_file_name)

# 在此添加模型的 MetaData 对象，以支持自动生成迁移。
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

from app.core.config import settings  # noqa: E402
from app.models import SQLModel  # noqa: E402

target_metadata = SQLModel.metadata

# 可根据 env.py 的需要读取其他配置值：
# my_important_option = config.get_main_option("my_important_option")
# ……以此类推。


def get_url():
    database_url = str(settings.DATABASE_URL)

    return database_url


def run_migrations_offline():
    """以离线模式执行迁移。

    此模式仅使用数据库 URL 配置上下文，不创建数据库引擎，
    因此无需提供 DBAPI。这里调用 context.execute() 时，
    给定内容会直接写入生成的脚本。
    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """以在线模式执行迁移。

    此模式会创建数据库引擎，并将数据库连接绑定到迁移上下文。
    """
    configuration = config.get_section(config.config_ini_section)
    assert configuration is not None
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
