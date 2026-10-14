import "client-only"

import { clearAccessToken, getAccessToken } from "@/lib/auth/token-storage"

const API_PREFIX = "/api/v1"

type ApiRequestOptions = Omit<RequestInit, "body"> & {
  auth?: boolean
  body?: BodyInit | object | null
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly payload: unknown
  ) {
    super(`API request failed with status ${status}`)
    this.name = "ApiError"
  }
}

function prepareBody(body: ApiRequestOptions["body"], headers: Headers) {
  if (body == null) {
    return undefined
  }

  if (
    typeof body === "string" ||
    body instanceof FormData ||
    body instanceof URLSearchParams ||
    body instanceof Blob ||
    body instanceof ArrayBuffer
  ) {
    return body
  }

  headers.set("Content-Type", "application/json")
  return JSON.stringify(body)
}

async function readResponse(response: Response): Promise<unknown> {
  if (response.status === 204) {
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

export async function apiFetch<T>(
  path: string,
  options: ApiRequestOptions = {}
): Promise<T> {
  const { auth = true, body, headers: initialHeaders, ...requestInit } = options
  const headers = new Headers(initialHeaders)

  if (auth) {
    const accessToken = getAccessToken()
    if (accessToken) {
      headers.set("Authorization", `Bearer ${accessToken}`)
    }
  }

  const response = await fetch(`${API_PREFIX}${path}`, {
    ...requestInit,
    body: prepareBody(body, headers),
    headers,
  })
  const payload = await readResponse(response)

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      clearAccessToken()
    }
    throw new ApiError(response.status, payload)
  }

  return payload as T
}
