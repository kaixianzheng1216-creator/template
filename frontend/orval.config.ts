import { loadEnvConfig } from "@next/env"
import { defineConfig } from "orval"

loadEnvConfig(process.cwd(), process.env.NODE_ENV !== "production")

const backendUrl = process.env.BACKEND_URL

if (!backendUrl) throw new Error("必须配置 BACKEND_URL")

export default defineConfig({
  api: {
    input: `${backendUrl}/api/v1/openapi.json`,
    output: {
      clean: true,
      client: "fetch",
      mode: "tags-split",
      target: "./lib/api/generated/endpoints",
      schemas: "./lib/api/generated/models",
      override: {
        header: (info) => [
          "由 orval 自动生成",
          "请勿手动编辑。",
          info.title,
          `OpenAPI 规范版本： ${info.version}`,
        ],
        fetch: { includeHttpResponseReturnType: false },
        mutator: {
          path: "./lib/api/client.ts",
          name: "apiFetch",
        },
      },
    },
  },
})
