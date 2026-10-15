import { clearAccessToken, getAccessToken } from "@/lib/auth/token-storage"

const DEFAULT_BACKEND_URL = "http://localhost:8000"
const NO_CONTENT_STATUS = 204
const UNAUTHORIZED_STATUS = 401

type ApiErrorPayload = {
  message?: string
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly payload: unknown
  ) {
    super(`API 请求失败，状态码：${status}`)
    this.name = "ApiError"
  }
}

export async function apiFetch<T>(
  url: string,
  options: RequestInit
): Promise<T> {
  const headers = new Headers(options.headers)

  const accessToken = getAccessToken()

  if (accessToken && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${accessToken}`)
  }

  const response = await fetch(resolveApiUrl(url), {
    ...options,
    headers,
  })

  const payload = await readResponse(response)

  if (!response.ok) {
    if (response.status === UNAUTHORIZED_STATUS) {
      clearAccessToken()
    }

    throw new ApiError(response.status, payload)
  }

  return payload as T
}

export function getApiErrorMessage(
  error: unknown,
  fallback = "操作失败，请稍后重试"
): string {
  if (!(error instanceof ApiError)) {
    return fallback
  }

  const payload = error.payload as ApiErrorPayload | null

  return payload?.message ?? fallback
}

function resolveApiUrl(url: string): string {
  if (typeof window !== "undefined") {
    return url
  }

  const backendUrl = (process.env.BACKEND_URL ?? DEFAULT_BACKEND_URL).replace(
    /\/$/,
    ""
  )

  return `${backendUrl}${url}`
}

async function readResponse(response: Response): Promise<unknown> {
  if (response.status === NO_CONTENT_STATUS) {
    return null
  }

  const text = await response.text()

  if (!text) {
    return null
  }

  if (response.headers.get("content-type")?.includes("application/json")) {
    return JSON.parse(text) as unknown
  }

  return text
}
