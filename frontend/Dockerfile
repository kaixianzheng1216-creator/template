FROM docker.m.daocloud.io/library/node:24-alpine AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

# 使用国内镜像
ENV NPM_CONFIG_REGISTRY=https://registry.npmmirror.com

RUN corepack enable

WORKDIR /app


FROM base AS dependencies

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

RUN pnpm install --frozen-lockfile


FROM dependencies AS development

COPY . .

CMD ["pnpm", "dev", "--hostname", "0.0.0.0"]


FROM dependencies AS build

ARG BACKEND_URL=http://localhost:8000

ENV BACKEND_URL=$BACKEND_URL
ENV NEXT_TELEMETRY_DISABLED=1

COPY . .

RUN pnpm build


FROM docker.m.daocloud.io/library/node:24-alpine AS production

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

WORKDIR /app

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

COPY --from=build /app/public ./public
COPY --from=build --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=build --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]
