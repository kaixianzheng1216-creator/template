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

前端统一通过 `lib/api/client.ts` 请求 `/api/v1`。登录成功后，JWT 保存在浏览器 `localStorage`，后续请求自动携带 `Authorization: Bearer <token>`。

认证封装位于：

* `lib/api/auth.ts`
* `lib/api/types.ts`
* `lib/auth/token-storage.ts`

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
