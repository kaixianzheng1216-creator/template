import "client-only"
import type { ErrorResponse } from "@/lib/api/generated/models"

export class ApiError extends Error {
  readonly status: number
  readonly retryAfter: number | undefined

  constructor(status: number, payload?: ErrorResponse, retryAfter?: number) {
    super(payload?.message ?? "请求失败，请稍后再试")
    this.name = "ApiError"
    this.status = status
    this.retryAfter = retryAfter
  }
}

export async function apiFetch<T>(
  url: string,
  options: RequestInit
): Promise<T> {
  const response = await fetch(url, options)

  if (!response.ok) {
    const payload = await response.json().catch(() => undefined)
    const seconds = Number(response.headers.get("Retry-After"))
    throw new ApiError(
      response.status,
      payload,
      Number.isFinite(seconds) && seconds > 0 ? Math.ceil(seconds) : undefined
    )
  }

  return response.status === 204 ? (undefined as T) : response.json()
}

export function isAccessError(error: unknown): boolean {
  return (
    error instanceof ApiError && (error.status === 401 || error.status === 403)
  )
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof ApiError && error.status === 429 && error.retryAfter) {
    const wait =
      error.retryAfter >= 60
        ? `${Math.ceil(error.retryAfter / 60)} 分钟`
        : `${error.retryAfter} 秒`
    return `操作暂受限，请在 ${wait}后重试`
  }
  return error instanceof ApiError ? error.message : "操作失败，请再试一次"
}
