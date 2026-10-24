# Next.js + FastAPI 项目

## 技术栈与功能

- ⚡ 使用 [**FastAPI**](https://fastapi.tiangolo.com) 构建 Python 后端 API。
  - 🧰 使用 [SQLModel](https://sqlmodel.tiangolo.com) 与 Python SQL 数据库交互（ORM）。
  - 🔍 使用 FastAPI 所依赖的 [Pydantic](https://docs.pydantic.dev) 进行数据校验和配置管理。
  - 💾 使用 [PostgreSQL](https://www.postgresql.org) 作为 SQL 数据库。
- ▲ 使用 [Next.js](https://nextjs.org)、TypeScript、Tailwind CSS 和 shadcn/ui 构建前端。
- 🔌 Next.js 通过同源 `/api/v1/*` 代理访问 FastAPI。
- 🐋 使用 [Docker Compose](https://www.docker.com) 运行本地服务和自托管部署。
- 🔐 使用 [Clerk](https://clerk.com) 管理注册、登录、密码和会话。
- 👤 Clerk 是用户资料、状态和角色的唯一事实来源；业务数据只保存稳定的 Clerk User ID。

### 交互式 API 文档

项目启动后，可通过 <http://localhost:8000/scalar> 查看 API 文档。

## 使用方法

点击本页面顶部的 **Use this template** 按钮创建新仓库。

## 后端开发

后端文档：[backend/README.md](./backend/README.md)。

## 前端开发

前端文档：[frontend/README.md](./frontend/README.md)。

## 部署

使用 Docker Compose 自托管部署：[deployment-docker-compose.md](./deployment-docker-compose.md)。

## 开发

通用开发文档：[development.md](./development.md)。

其中包括 Next.js、FastAPI、Docker Compose 和 `.env` 配置等内容。
