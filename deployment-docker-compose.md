# FastAPI 项目——Docker Compose 部署指南

可以使用 Docker Compose 将项目部署到自己的远程服务器。前端使用 `3000` 端口，后端 API 使用 `8000` 端口。

## 准备工作

* 准备一台可用的远程服务器。
* 在远程服务器上安装并配置 [Docker](https://docs.docker.com/engine/install/)（使用 Docker Engine，而不是 Docker Desktop）。

## 复制代码

```bash
rsync -av --exclude=".git/" --filter=":- .gitignore" ./ root@your-server.example.com:/root/code/app/
```

`--filter=":- .gitignore"` 选项会让 `rsync` 使用与 Git 相同的忽略规则，从而排除 Python 虚拟环境等文件。

## 配置应用

### 环境变量

设置允许访问 API 的前端来源、项目名称和第一个超级用户的用户名：

```bash
export FRONTEND_HOST=http://your-server.example.com:8000
export PROJECT_NAME="Full Stack FastAPI Project"
export FIRST_SUPERUSER=admin
```

还可以根据需要配置以下环境变量：

* `SENTRY_DSN`：Sentry 的 DSN。

### 密钥

为数据库密码、令牌签名密钥和第一个超级用户密码生成并设置安全的值：

```bash
export POSTGRES_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export FIRST_SUPERUSER_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

## 部署

```bash
cd /root/code/app/
docker compose -f compose.yml -f compose.deploy.yml build
docker compose -f compose.yml -f compose.deploy.yml run --rm backend bash scripts/prestart.sh
docker compose -f compose.yml -f compose.deploy.yml up -d
```

`compose.deploy.yml` 会在共享的 `compose.yml` 配置基础上添加生产端口和自动重启策略。显式列出这两个文件，可以排除 `compose.override.yml` 中的本地开发配置。

## 使用 GitHub Actions 部署

内置的 `.github/workflows/deploy-docker-compose.yml` 工作流会在 GitHub Actions 中手动触发时，在服务器上运行部署命令。

仅应在你信任仓库贡献者和工作流代码的仓库中使用自托管 Runner。GitHub 建议将自托管 Runner 用于私有仓库，因为工作流会直接在 Runner 所在机器上执行。

### 配置仓库变量和密钥

进入仓库的 **Settings** > **Secrets and variables** > **Actions**，添加以下仓库变量：

* `FRONTEND_HOST`
* `PROJECT_NAME`
* `FIRST_SUPERUSER`

如需启用 Sentry，请添加可选的仓库变量 `SENTRY_DSN`。

添加以下仓库密钥：

* `POSTGRES_PASSWORD`
* `SECRET_KEY`
* `FIRST_SUPERUSER_PASSWORD`

### 安装自托管 Runner

在服务器上创建专用用户，并授予其访问 Docker 的权限：

```bash
sudo adduser github
sudo usermod -aG docker github
sudo su - github
```

在 GitHub 仓库中进入 **Settings** > **Actions** > **Runners**，选择 **New self-hosted runner**，选择 Linux，然后按照 GitHub 提供的命令下载、配置并注册 Runner。请将其安装到 `/home/github/actions-runner`。

注册 Runner 后，退出 `github` 用户会话，并将 Runner 安装为系统服务：

```bash
exit
cd /home/github/actions-runner
sudo ./svc.sh install github
sudo ./svc.sh start
sudo ./svc.sh status
```

请参阅 GitHub 关于[添加自托管 Runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners) 和[将 Runner 配置为服务](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/configure-the-application?platform=linux)的指南。

### 运行部署

Runner 上线后，打开仓库的 **Actions** 选项卡，选择 **Deploy with Docker Compose**，然后选择 **Run workflow**。

## 访问地址

后端 API：`http://your-server.example.com:8000`

前端：`http://your-server.example.com:3000`

交互式 API 文档：`http://your-server.example.com:8000/docs`
