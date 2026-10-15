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

## 访问地址

后端 API：`http://your-server.example.com:8000`

前端：`http://your-server.example.com:3000`

交互式 API 文档：`http://your-server.example.com:8000/docs`
