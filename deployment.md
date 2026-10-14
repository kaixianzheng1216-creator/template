# FastAPI 项目——部署指南

使用项目内置的 GitHub Actions 工作流，将项目部署到 [FastAPI Cloud](https://fastapicloud.com)。

## 创建 FastAPI Cloud 应用

在 FastAPI Cloud 中创建一个应用，并将其[应用目录](https://fastapicloud.com/docs/builds-and-deployments/application-directory/)设置为 `backend`。

使用 [Neon](https://fastapicloud.com/docs/integrations/neon-integration/) 或 [Supabase](https://fastapicloud.com/docs/integrations/supabase-integration/) 集成连接 PostgreSQL 数据库。这两种集成都会自动配置 `DATABASE_URL` 密钥。使用其他 PostgreSQL 服务提供商时，也可以手动配置 `DATABASE_URL`。

## 配置应用

### 环境变量

在 FastAPI Cloud 应用中添加以下必需的[环境变量](https://fastapicloud.com/docs/builds-and-deployments/environment-variables/)：

* `PROJECT_NAME`：项目名称，用于 API 文档。
* `FIRST_SUPERUSER`：第一个超级用户的用户名。
* `FRONTEND_HOST`：允许访问 API 的前端来源地址。

如需启用 Sentry，请配置 `SENTRY_DSN`。

### 密钥

添加以下必需配置，并将其标记为密钥：

* `SECRET_KEY`：用于签署安全令牌的密钥。
* `FIRST_SUPERUSER_PASSWORD`：第一个超级用户的密码。
* `DATABASE_URL`：PostgreSQL 连接 URL；使用数据库集成时会自动配置。

可以使用以下命令为 `SECRET_KEY` 和 `FIRST_SUPERUSER_PASSWORD` 生成安全的值：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 配置持续部署

内置的 `.github/workflows/deploy.yml` 工作流会在变更推送到 `master` 时准备数据库并部署后端。也可以从 **Actions** 选项卡手动运行该工作流。

登录 FastAPI Cloud，然后将[部署令牌](https://fastapicloud.com/docs/advanced-features/deploy-tokens/)和应用 ID 配置为 GitHub 仓库密钥：

```bash
uv run fastapi login
uv run fastapi cloud setup-ci --secrets-only --app-id <your-app-id>
```

如果已安装 GitHub CLI 并完成身份验证，该命令会自动配置 `FASTAPI_CLOUD_TOKEN` 和 `FASTAPI_CLOUD_APP_ID`。否则，命令会输出这些值，以便在仓库的 **Settings** > **Secrets and variables** > **Actions** 中添加。

工作流会在部署前运行数据库迁移并创建第一个超级用户。在仓库的 **Settings** > **Secrets and variables** > **Actions** 页面中，添加以下仓库变量：

* `PROJECT_NAME`
* `FIRST_SUPERUSER`

添加以下仓库密钥：

* `DATABASE_URL`
* `SECRET_KEY`
* `FIRST_SUPERUSER_PASSWORD`

请使用与 FastAPI Cloud 中相同的值。`DATABASE_URL` 应使用数据库服务提供商给出的连接 URL。数据库必须能够被 GitHub 托管的 Runner 访问，以便准备步骤连接数据库。

部署工作流执行以下步骤：

1. 运行 `backend/scripts/prestart.sh`，应用数据库迁移并创建第一个超级用户。
2. 使用 `uv run fastapi deploy` 部署项目。

## 访问地址

请将 `your-app.fastapicloud.dev` 替换为 FastAPI Cloud 应用的 URL。

后端 API：`https://your-app.fastapicloud.dev`

交互式 API 文档：`https://your-app.fastapicloud.dev/docs`

## Docker Compose

如需部署到自己的服务器，请参阅 [Docker Compose 部署指南](./deployment-docker-compose.md)。

## GitHub 仓库自动化

安装以下 GitHub Apps，以启用项目内置的仓库自动化功能：

* [PR Push](https://github.com/apps/pr-push) 允许提交前检查工作流将自动修复推送到拉取请求分支。
* [PR Submit](https://github.com/apps/pr-submit) 允许 **Bump pre-commit hooks** 和 **Prepare Release** 工作流创建拉取请求。
