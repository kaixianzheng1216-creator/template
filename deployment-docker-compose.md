# FastAPI 项目——Docker Compose 部署指南

可以使用 Docker Compose 将项目部署到自己的远程服务器。应用通过前端的 `3000` 端口提供服务，后端只在 Compose 内部网络中使用。

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

通过服务器的环境变量或密钥管理服务提供 `PROJECT_NAME`、`FRONTEND_URL`、`NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` 和 `CLERK_SECRET_KEY`。生产环境必须使用 Clerk 正式实例的真实配置，不要提交到仓库。管理员角色在 Clerk `publicMetadata.role` 中配置，并通过会话令牌的 `metadata` 声明提供给应用。

### 密钥

为数据库生成并设置安全密码：

```bash
export POSTGRES_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

## 部署

```bash
cd /root/code/app/
docker compose -f compose.yml -f compose.deploy.yml build
docker compose -f compose.yml -f compose.deploy.yml up -d
```

`migrate` 服务会在后端启动前自动执行数据库迁移。`compose.deploy.yml` 会在共享的 `compose.yml` 配置基础上添加生产端口和自动重启策略。显式列出这两个文件，可以排除 `compose.override.yml` 中的本地开发配置。

## 访问地址

前端：`http://your-server.example.com:3000`
