import "client-only"
import type { ErrorResponse } from "@/lib/api/generated/models"

export class ApiError extends Error {
  readonly status: number

  constructor(status: number, payload?: ErrorResponse) {
    super(payload?.message ?? "请求失败，请稍后再试")
    this.name = "ApiError"
    this.status = status
  }
}

export async function apiFetch<T>(
  url: string,
  options: RequestInit
): Promise<T> {
  const response = await fetch(url, options)

  if (!response.ok) {
    const payload = await response.json().catch(() => undefined)
    throw new ApiError(response.status, payload)
  }

  return response.status === 204 ? (undefined as T) : response.json()
}

export function isAccessError(error: unknown): boolean {
  return (
    error instanceof ApiError && (error.status === 401 || error.status === 403)
  )
}

export function getApiErrorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : "操作失败，请再试一次"
}
