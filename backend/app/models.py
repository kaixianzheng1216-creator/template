"""集中导入数据库模型，供 Alembic 注册元数据。"""

from sqlmodel import SQLModel

from app.items.models import Item

__all__ = ["Item", "SQLModel"]
