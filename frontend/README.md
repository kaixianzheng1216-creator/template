# Next.js 前端

本项目使用 Next.js App Router、TypeScript、Tailwind CSS 和 shadcn/ui。

## 本地开发

先启动 FastAPI，然后在本目录安装依赖并启动前端：

```bash
pnpm install
pnpm dev
```

访问 <http://localhost:3000>。Next.js 会将 `/api/*` 请求代理到显式配置的 `BACKEND_URL`。

复制 `.env.example` 为 `.env.local`，填写项目名称、Clerk 配置和后端地址。

## API 与认证

前端使用 Orval，根据 FastAPI 的 OpenAPI 文档生成类型安全的模型和请求函数。后端启动后执行：

```bash
pnpm api:generate
```

生成结果位于 `lib/api/generated`，不要手动修改。后端接口发生变化后，应重新执行生成命令并提交生成结果。

Orval 直接从 `BACKEND_URL` 指向的后端读取 OpenAPI 定义。

生成器使用 `@next/env` 按 Next.js 的规则加载环境文件，与开发服务共用 `.env.local` 中的 `BACKEND_URL`；默认按开发环境加载，设置 `NODE_ENV=production` 时按生产环境加载。

`lib/api/client.ts` 是生成客户端共用的请求层，只负责解析响应和统一抛出 API 错误。浏览器请求通过 Next.js 代理访问后端。

Clerk 负责登录、注册、密码和会话。浏览器通过同源 `/api` 请求 FastAPI，Clerk 会话 Cookie 会随请求发送；前端不自行保存访问令牌。

登录和注册路径统一定义在 `lib/auth-routes.ts`，由 ClerkProvider 与中间件共用；认证完成默认进入 `/contents`。这些固定路由不使用环境变量，开发与生产保持一致。

查询缓存按 Clerk 会话隔离，会话变化时重建。侧边栏和用户列表都展示 Clerk 当前资料；管理员权限来自 Clerk 会话中的 `metadata.role`，用户列表、角色和封禁状态由后端实时调用 Clerk Backend API。

OpenAPI 生成配置位于 `orval.config.ts`。

## UI 组件约定

项目预装 shadcn/ui 全部 UI 组件。即使暂未被业务页面引用，也保留 `components/ui` 中的组件及其依赖；代码收敛仅针对业务实现，不按使用率裁剪组件库。

补齐预装组件时保留已有文件，不覆盖项目内的定制：

```bash
pnpm exec shadcn add --all
```

单独添加组件：

```bash
pnpm exec shadcn add <component>
```

## 质量检查

```bash
pnpm check
pnpm build
```
