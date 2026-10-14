# FastAPI 项目——前端

前端使用 [Vite](https://vitejs.dev/)、[React](https://react.dev/)、[TypeScript](https://www.typescriptlang.org/)、[TanStack Query](https://tanstack.com/query)、[TanStack Router](https://tanstack.com/router)、[Tailwind CSS](https://tailwindcss.com/) 和 [shadcn/ui](https://ui.shadcn.com/) 构建。

## 环境要求

- [Bun](https://bun.sh/)

## 快速开始

在项目根目录安装依赖并启动前端开发服务器：

```bash
bun install
bun run dev
```

然后在浏览器中打开 <http://localhost:5173/>。

确保 Docker Compose 中的 PostgreSQL 正在运行，然后在 `backend` 目录执行 `uv run bash scripts/prestart.sh` 和 `uv run fastapi dev`。完整配置方式请参阅 [../development.md](../development.md)。

如需通过 FastAPI 提供前端服务，请在 `frontend` 目录执行 `bun run build`，然后打开 `http://localhost:8000`。

其他可用命令请查看 `frontend/package.json`。

## 移除前端

如果要开发仅包含 API 的应用，可以按照以下步骤移除前端：

* 删除 `./frontend` 目录。

* 在 `backend/app/main.py` 文件中删除 `app.frontend()` 调用。

* 在 `backend/Dockerfile` 文件中删除前端构建阶段和 `COPY --from=frontend-build` 指令。

* 在 `compose.override.yml` 文件中删除 `playwright` 服务。

* 在 `.github/workflows/deploy.yml` 文件中删除 **Set up Bun**、**Install frontend dependencies** 和 **Build frontend** 步骤。

* 在 `.fastapicloudignore` 文件中删除 `!backend/app/frontend/` 条目。

完成，现在得到的就是一个仅包含 API 的应用。🤓

## 生成客户端

### 自动生成

* 在项目根目录运行脚本：

```bash
bash ./scripts/generate-client.sh
```

* 提交生成的变更。

### 手动生成

* 确保后端正在运行。

* 从 `http://localhost:8000/api/v1/openapi.json` 下载 OpenAPI JSON 文件，并将其复制到 `frontend` 根目录下的新文件 `openapi.json` 中。

* 执行以下命令生成前端客户端：

```bash
bun run generate-client
```

* 提交生成的变更。

只要后端变更会影响 OpenAPI Schema，就应重新生成客户端。

## 使用远程 API

默认情况下，构建后的前端与 FastAPI 应用使用相同来源。如果希望在运行 Vite 开发服务器时使用远程 API，可以将环境变量 `VITE_API_URL` 设置为远程 API 的 URL。例如，可以在 `frontend/.env` 文件中设置：

```env
VITE_API_URL=https://my-domain.example.com
```

之后运行前端时，它将使用该 URL 作为 API 的基础 URL。

## 代码结构

前端代码结构如下：

* `frontend/src`——主要前端代码。
* `frontend/public`——静态资源。
* `frontend/src/client`——生成的 OpenAPI 客户端。
* `frontend/src/components`——前端组件，包括位于 `frontend/src/components/ui` 中的 shadcn/ui 组件。
* `frontend/src/hooks`——自定义 Hooks。
* `frontend/src/lib`——共享前端工具。
* `frontend/src/routes`——前端路由和页面。

## 使用 Playwright 进行端到端测试

前端包含一组初始 Playwright 端到端测试。运行测试前，需要先启动 Docker Compose 服务栈：

```bash
docker compose run --rm backend bash scripts/prestart.sh
docker compose up -d --wait backend
```

然后运行测试：

```bash
bunx playwright test
```

也可以在 UI 模式下运行测试，以查看浏览器并与运行中的测试交互：

```bash
bunx playwright test --ui
```

如需停止并删除 Docker Compose 服务栈，同时清理测试产生的数据，请执行：

```bash
docker compose down -v
```

如需更新测试，请进入测试目录，根据需要修改现有测试文件或添加新文件。

有关编写和运行 Playwright 测试的更多信息，请参阅官方 [Playwright 文档](https://playwright.dev/docs/intro)。
