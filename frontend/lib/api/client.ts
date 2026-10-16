import "client-only"

import { clearAccessToken, getAccessToken } from "@/lib/auth/token-storage"

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

  const response = await fetch(url, {
    ...options,
    headers,
  })

  const payload =
    response.status === NO_CONTENT_STATUS ? undefined : await response.json()

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

  const payload = error.payload as ApiErrorPayload | undefined

  return payload?.message ?? fallback
}
