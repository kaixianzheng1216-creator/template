"""集中导入数据库模型，供 Alembic 注册元数据。"""

from sqlmodel import SQLModel

from app.contents.models import Content

__all__ = ["Content", "SQLModel"]
