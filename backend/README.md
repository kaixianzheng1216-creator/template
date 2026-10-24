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
$ uv run alembic upgrade head
$ uv run uvicorn app.main:app --reload
```

API 地址为 `http://localhost:8000`，Swagger UI 位于 `http://localhost:8000/docs`，Scalar 文档位于 `http://localhost:8000/scalar`。

后端使用 Clerk 验证会话，Clerk 是用户资料、角色和封禁状态的唯一事实来源。数据库不保存用户副本；业务数据直接记录 Clerk User ID，用户列表和管理操作通过 Clerk Backend API 完成，因此本地开发不依赖 Webhook 或公网回调地址。运行前需要按照根目录 `.env.example` 配置项目名称、前端地址、Clerk 密钥和数据库连接。

管理员角色保存在 Clerk 用户的 `publicMetadata.role`。在 Clerk Dashboard 的 **Sessions > Customize session token** 中加入以下声明，让前后端可以直接从已验证的会话判断角色：

```json
{
  "metadata": "{{user.public_metadata}}"
}
```

再为初始管理员设置 `publicMetadata` 为 `{ "role": "admin" }`，并重新登录以刷新会话令牌。普通用户使用 `{ "role": "member" }`。

## 常规工作流程

在 `./backend/` 中通过 `uv run` 执行后端命令。请将 `backend` 标记为源码根目录，并让编辑器使用项目根目录下的虚拟环境解释器：Linux/macOS 为 `.venv/bin/python`，Windows 为 `.venv\\Scripts\\python.exe`。

在各业务模块的 `models.py` 中维护 SQLModel 数据库模型，在 `router.py` 中定义 API 端点，在 `service.py` 中编写业务逻辑和数据库操作。

## 使用 Docker Compose 运行后端

要在 Docker Compose 中运行后端，请执行：

```console
$ docker compose watch
```

`migrate` 服务会在后端启动前自动执行数据库迁移。应用地址为 `http://localhost:8000`。

### Docker Compose 覆盖配置

`compose.override.yml` 包含本地开发所需的端口发布、源码同步、镜像自动重建和后端重新加载设置。不显式指定配置文件而直接运行 `docker compose` 时，Docker Compose 会自动应用该文件。

要在后端容器中打开终端，请执行：

```console
$ docker compose exec backend bash
```

## 质量检查

在 `backend` 目录执行：

```bash
uv run mypy app
uv run ruff check app
uv run ruff format app --check
```

## 数据库迁移

模板仅提供面向空数据库的最终初始化基线，不包含旧认证结构的升级路径。项目开始使用后，应保留已执行的迁移，通过新增迁移演进结构，不再改写初始化基线。

每次修改模型后，请务必为模型创建一个迁移版本，并使用该版本升级数据库。在 `backend` 目录中，通过 `uv` 针对 PostgreSQL 容器运行 Alembic：

* Alembic 已配置为从 `./backend/app/models.py` 导入 SQLModel 模型。

* 修改模型后（例如添加字段），创建一个迁移版本：

```console
$ uv run alembic revision --autogenerate -m "为用户模型添加 last_name 字段"
```

* 将 Alembic 目录中生成的文件提交到 Git 仓库。

* 创建迁移版本后，在数据库中运行迁移（该操作会实际修改数据库）：

```console
$ uv run alembic upgrade head
```
