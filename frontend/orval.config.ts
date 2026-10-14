import { defineConfig } from "orval"

const OPENAPI_URL = "http://localhost:8000/api/v1/openapi.json"

export default defineConfig({
  api: {
    input: OPENAPI_URL,
    output: {
      clean: true,
      client: "fetch",
      mode: "tags-split",
      target: "./lib/api/generated/endpoints",
      schemas: "./lib/api/generated/models",
      override: {
        mutator: {
          path: "./lib/api/client.ts",
          name: "apiFetch",
        },
        fetch: {
          includeHttpResponseReturnType: false,
        },
      },
    },
  },
})
