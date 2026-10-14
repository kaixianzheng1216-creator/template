# FastAPI 全栈项目模板

[![测试 Docker Compose](../../actions/workflows/test-docker-compose.yml/badge.svg)](../../actions/workflows/test-docker-compose.yml)
[![测试后端](../../actions/workflows/test-backend.yml/badge.svg)](../../actions/workflows/test-backend.yml)

## 技术栈与功能

- ⚡ 使用 [**FastAPI**](https://fastapi.tiangolo.com) 构建 Python 后端 API。
  - 🧰 使用 [SQLModel](https://sqlmodel.tiangolo.com) 与 Python SQL 数据库交互（ORM）。
  - 🔍 使用 FastAPI 所依赖的 [Pydantic](https://docs.pydantic.dev) 进行数据校验和配置管理。
  - 💾 使用 [PostgreSQL](https://www.postgresql.org) 作为 SQL 数据库。
- 🚀 使用 [React](https://react.dev) 构建前端。
  - 🧩 前端会构建到后端应用中，由 FastAPI 在与 API 相同的域名下提供服务。
  - 💃 使用 TypeScript、Hooks、[Vite](https://vitejs.dev) 及现代前端技术栈中的其他工具。
  - 🎨 使用 [Tailwind CSS](https://tailwindcss.com) 和 [shadcn/ui](https://ui.shadcn.com) 构建前端组件。
  - 🤖 自动生成前端 API 客户端。
  - 🧪 使用 [Playwright](https://playwright.dev) 进行端到端测试。
  - 🦇 支持深色模式。
- ☁️ 使用 [FastAPI Cloud](https://fastapicloud.com) 进行部署。
- 🐋 使用 [Docker Compose](https://www.docker.com) 运行本地服务和自托管部署。
  - 📞 使用 [Traefik](https://traefik.io) 作为反向代理，并自动配置 HTTPS。
- 🔒 默认采用安全的密码哈希方案。
- 🔑 支持 JWT（JSON Web Token）身份认证。
- 📫 支持通过电子邮件找回密码。
- ✉️ 使用 [React Email](https://react.email) 编写邮件模板。
- 📬 使用 [Mailpit](https://mailpit.axllent.org) 测试开发环境中的邮件。
- ✅ 使用 [Pytest](https://pytest.org) 进行测试。
- 🏭 基于 GitHub Actions 实现 CI（持续集成）和 CD（持续部署）。

### 控制台登录

![控制台登录截图](img/login.png)

### 控制台——管理员

![管理员控制台截图](img/dashboard.png)

### 控制台——项目

![项目管理页面截图](img/dashboard-items.png)

### 控制台——深色模式

![深色模式控制台截图](img/dashboard-dark.png)

### React Email 模板

![邮件模板截图](img/react-email.png)

### Mailpit——本地邮件测试

![Mailpit 截图](img/mailpit.png)

### 交互式 API 文档

![API 文档截图](img/docs.png)

## 使用方法

点击本页面顶部的 **Use this template** 按钮创建新仓库。

## 后端开发

后端文档：[backend/README.md](./backend/README.md)。

## 前端开发

前端文档：[frontend/README.md](./frontend/README.md)。

## 部署

FastAPI Cloud 部署：[deployment.md](./deployment.md)。

使用 Docker Compose 自托管部署：[deployment-docker-compose.md](./deployment-docker-compose.md)。

## 开发

通用开发文档：[development.md](./development.md)。

其中包括本地 FastAPI 与 Vite 开发流程、Docker Compose 服务、`.env` 配置等内容。
