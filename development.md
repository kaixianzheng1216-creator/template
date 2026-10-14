# FastAPI 项目——开发指南

## 本地开发

本地开发时，通过 Docker Compose 运行 PostgreSQL，并在本机运行 FastAPI 开发服务器。

启动依赖服务：

```bash
docker compose up -d db
```

然后进入 `backend` 目录，安装依赖并准备数据库：

```bash
uv sync
uv run bash scripts/prestart.sh
```

启动 FastAPI 开发服务器：

```bash
uv run fastapi dev
```

现在可以访问以下地址：

后端 API：<http://localhost:8000>

由 Swagger UI 提供的自动交互式 API 文档：<http://localhost:8000/docs>

## 使用 Docker Compose 运行后端

要在 Docker Compose 中运行后端，请执行：

```bash
docker compose run --rm backend bash scripts/prestart.sh
docker compose watch
```

现在可以访问以下地址：

后端 API：<http://localhost:8000>

由 Swagger UI 提供的自动交互式 API 文档：<http://localhost:8000/docs>

启动 Compose 后端前，请停止本地运行的 FastAPI 服务器，因为两者都会使用 `8000` 端口。

**注意**：首次启动服务栈时，所有服务可能需要一分钟才能准备就绪。可以使用 `docker compose logs` 查看状态，或使用 `docker compose logs backend` 单独查看后端服务。

## Docker Compose 文件和环境变量

主配置文件 `compose.yml` 包含整个服务栈共享的配置，Docker Compose 会自动加载它。

`compose.override.yml` 添加本地开发配置，例如将源码作为卷挂载。Docker Compose 也会自动加载该文件，并将其配置叠加到 `compose.yml` 之上。

`compose.deploy.yml` 包含部署专用配置，包括端口发布和自动重启。部署应用时，需要将它与 `compose.yml` 显式组合使用。

后端从 `.env` 文件读取本地配置。Docker Compose 也使用该文件进行变量插值，并将各容器所需的配置传入容器。

修改变量后，请务必重启服务栈：

```bash
docker compose watch
```

## `.env` 文件

受版本控制的 `.env` 文件包含本地开发默认值、密码及其他配置。其中的主机名使用 `localhost`，供运行在本机上的进程访问。Docker Compose 会将数据库主机名覆盖为对应的 Compose 服务名。

请勿在 `.env` 中保存部署密钥。请按照 [FastAPI Cloud 部署指南](./deployment.md)或 [Docker Compose 部署指南](./deployment-docker-compose.md)中的说明配置密钥。

## 提交前钩子与代码检查

本项目使用 [prek](https://prek.j178.dev/) 进行代码检查和格式化，它是 [pre-commit](https://pre-commit.com/) 的现代替代方案。

项目根目录中的 `.pre-commit-config.yaml` 文件包含相关配置。

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
