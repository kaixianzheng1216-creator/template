# FastAPI 项目——开发指南

## 本地开发

### 配置 Clerk

先复制根目录的环境变量模板：

```bash
cp .env.example .env
```

然后在 Clerk 创建应用，启用邮箱、密码和 Google 登录，并填写本地 `.env` 中留空的 Clerk 配置和数据库密码。

Clerk 是用户资料、角色和封禁状态的唯一事实来源，应用不复制用户表，也不依赖 Webhook。在 Clerk Dashboard 的 **Sessions > Customize session token** 中配置：

```json
{
  "metadata": "{{user.public_metadata}}"
}
```

然后把首位管理员的 `publicMetadata` 设置为 `{ "role": "admin" }` 并重新登录。其他用户使用 `{ "role": "member" }`。内容只保存稳定的 Clerk User ID，因此姓名和邮箱变化不会改变内容归属。

直接运行 Next.js 时，还需要把 `frontend/.env.example` 复制为 `frontend/.env.local`，并填写项目名称、后端地址以及相同的 Clerk 公钥和密钥。密钥只能用于本地环境，不要提交。

本地开发时，通过 Docker Compose 运行 PostgreSQL，并分别运行 FastAPI 与 Next.js 开发服务器。

启动依赖服务：

```bash
docker compose up -d db
```

然后进入 `backend` 目录，安装依赖并准备数据库：

```bash
uv sync
uv run alembic upgrade head
```

启动 FastAPI 开发服务器：

```bash
uv run uvicorn app.main:app --reload
```

现在可以访问以下地址：

后端 API：<http://localhost:8000>

由 Swagger UI 提供的自动交互式 API 文档：<http://localhost:8000/docs>

由 Scalar 提供的现代交互式 API 文档：<http://localhost:8000/scalar>

另开一个终端启动前端：

```bash
cd frontend
pnpm install
pnpm dev
```

前端地址：<http://localhost:3000>

Next.js 会把 `/api/*` 请求代理到显式配置的 `BACKEND_URL`。

## 使用 Docker Compose 运行完整应用

要在 Docker Compose 中运行数据库、后端和前端，请执行：

```bash
docker compose watch
```

`migrate` 服务会在后端启动前自动执行数据库迁移。

现在可以访问以下地址：

后端 API：<http://localhost:8000>

前端：<http://localhost:3000>

由 Swagger UI 提供的自动交互式 API 文档：<http://localhost:8000/docs>

由 Scalar 提供的现代交互式 API 文档：<http://localhost:8000/scalar>

启动 Compose 后端前，请停止本地运行的 FastAPI 服务器，因为两者都会使用 `8000` 端口。

**注意**：首次启动服务栈时，所有服务可能需要一分钟才能准备就绪。可以使用 `docker compose logs` 查看状态，或使用 `docker compose logs backend` 单独查看后端服务。

## Docker Compose 文件和环境变量

主配置文件 `compose.yml` 包含整个服务栈共享的配置，Docker Compose 会自动加载它。

`compose.override.yml` 添加本地开发配置，通过 Watch 同步源码，在依赖文件变化时重建镜像。Docker Compose 会自动加载该文件，并将其配置叠加到 `compose.yml` 之上。

`compose.deploy.yml` 包含部署专用配置，包括端口发布和自动重启。部署应用时，需要将它与 `compose.yml` 显式组合使用。

后端从 `.env` 文件读取本地配置。Docker Compose 也使用该文件进行变量插值，并将各容器所需的配置传入容器。

修改变量后，请务必重启服务栈：

```bash
docker compose watch
```

## `.env` 文件

受版本控制的 `.env.example` 是本地配置模板；真正的 `.env` 已被 Git 忽略。其中的主机名使用 `localhost`，供运行在本机上的进程访问。Docker Compose 会将数据库主机名覆盖为对应的 Compose 服务名。

`.env` 只能保存本地开发配置。部署时，请按照 [Docker Compose 部署指南](./deployment-docker-compose.md)单独配置密钥。

## 提交前钩子与代码检查

本项目使用 [prek](https://prek.j178.dev/) 进行代码检查和格式化，它是 [pre-commit](https://pre-commit.com/) 的现代替代方案。

项目根目录中的 `.pre-commit-config.yaml` 只运行 Ruff、Mypy 和前端 `check`。

### 安装 `prek` 以自动运行

`prek` 已包含在项目依赖中。

在项目根目录安装 Git 钩子，使 `prek` 在每次提交前自动运行：

```bash
uv run prek install -f
```

如果之前已安装过 `pre-commit` 钩子，`-f` 参数会强制执行安装。

此后每次尝试提交，例如执行：

```bash
git commit
```

`prek` 都会检查并格式化即将提交的代码。如果它修改了任何文件，请先将这些文件重新添加到 Git，再进行提交。

### 手动运行 `prek`

也可以在项目根目录手动对所有文件运行 `prek`：

```bash
uv run prek run --all-files
```
