# Next.js 前端

本项目使用 Next.js App Router、TypeScript、Tailwind CSS 和 shadcn/ui。

## 本地开发

先启动 FastAPI，然后在本目录安装依赖并启动前端：

```bash
pnpm install
pnpm dev
```

访问 <http://localhost:3000>。Next.js 会将 `/api/*` 请求代理到 `BACKEND_URL`，默认值为 `http://localhost:8000`。

如需覆盖后端地址，复制 `.env.example` 为 `.env.local` 并修改：

```env
BACKEND_URL=http://localhost:8000
```

## API 与认证

前端使用 Orval，根据 FastAPI 的 OpenAPI 文档生成类型安全的模型和请求函数。后端启动后执行：

```bash
pnpm api:generate
```

生成结果位于 `lib/api/generated`，不要手动修改。后端接口发生变化后，应重新执行生成命令并提交生成结果。

`lib/api/client.ts` 是生成客户端共用的请求层，只负责解析响应和统一抛出 API 错误。浏览器请求通过 Next.js 代理访问后端，服务端请求直接使用 `BACKEND_URL`。

认证逻辑独立放在 `lib/api/auth.ts`。登录成功后，JWT 暂时保存在浏览器 `localStorage`，仅由认证模块读取和携带。

认证封装位于：

- `lib/api/auth.ts`
- `lib/auth/token-storage.ts`

OpenAPI 生成配置位于 `orval.config.ts`。

## 添加组件

在本目录执行：

```bash
pnpm dlx shadcn@latest add <component>
```

## 质量检查

```bash
pnpm lint
pnpm typecheck
pnpm build
```
