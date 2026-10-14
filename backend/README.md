# FastAPI 项目——后端

## 环境要求

* [Docker](https://www.docker.com/)。
* 用于 Python 包和环境管理的 [uv](https://docs.astral.sh/uv/)。

## 本地开发

在本地运行后端，并连接到 Docker Compose 中的 PostgreSQL。

在项目根目录启动 PostgreSQL：

```console
$ docker compose up -d db
```

然后进入 `./backend/`，安装依赖、准备数据库并启动开发服务器：

```console
$ uv sync
$ uv run bash scripts/prestart.sh
$ uv run fastapi dev
```

API 地址为 `http://localhost:8000`，Swagger UI 位于 `http://localhost:8000/docs`，Scalar 文档位于 `http://localhost:8000/scalar`。

## 常规工作流程

在 `./backend/` 中通过 `uv run` 执行后端命令。请确保编辑器使用项目根目录下的 Python 解释器 `.venv/bin/python`。

在 `./backend/app/models.py` 中修改或添加数据及 SQL 表对应的 SQLModel 模型，在 `./backend/app/api/` 中编写 API 端点，在 `./backend/app/crud.py` 中编写 CRUD（创建、读取、更新、删除）工具函数。

## VS Code

项目已经包含通过 VS Code 调试器运行后端的配置，因此可以使用断点、暂停程序并查看变量等功能。

## 使用 Docker Compose 运行后端

要在 Docker Compose 中运行后端，请执行：

```console
$ docker compose run --rm backend bash scripts/prestart.sh
$ docker compose watch
```

应用地址为 `http://localhost:8000`。

### Docker Compose 覆盖配置

`compose.override.yml` 包含本地开发所需的端口发布、源码同步、镜像自动重建和后端重新加载设置。不显式指定配置文件而直接运行 `docker compose` 时，Docker Compose 会自动应用该文件。

要在后端容器中打开 Shell，请执行：

```console
$ docker compose exec backend bash
```

## 数据库迁移

每次修改模型后，请务必为模型创建一个迁移版本，并使用该版本升级数据库。在 `backend` 目录中，通过 `uv` 针对 PostgreSQL 容器运行 Alembic：

* Alembic 已配置为从 `./backend/app/models.py` 导入 SQLModel 模型。

* 修改模型后（例如添加字段），创建一个迁移版本：

```console
$ uv run alembic revision --autogenerate -m "Add column last_name to User model"
```

* 将 Alembic 目录中生成的文件提交到 Git 仓库。

* 创建迁移版本后，在数据库中运行迁移（该操作会实际修改数据库）：

```console
$ uv run alembic upgrade head
```

如果完全不想使用数据库迁移，请在 `./backend/app/core/db.py` 文件中取消以下结尾代码的注释：

```python
SQLModel.metadata.create_all(engine)
```

并注释掉 `scripts/prestart.sh` 文件中包含以下内容的行：

```console
$ alembic upgrade head
```

如果不想使用默认模型，希望在没有任何历史迁移版本的情况下从头删除或修改它们，可以删除 `./backend/app/alembic/versions/` 下的迁移版本文件（`.py` Python 文件），然后按上述方式创建第一个迁移。
