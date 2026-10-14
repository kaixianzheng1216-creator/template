const DEFAULT_BACKEND_URL = "http://localhost:8000"
const NO_CONTENT_STATUS = 204

export class ApiError<TPayload = unknown> extends Error {
  constructor(
    public readonly status: number,
    public readonly payload: TPayload
  ) {
    super(`API 请求失败，状态码：${status}`)
    this.name = "ApiError"
  }
}

export async function apiFetch<T>(
  url: string,
  options: RequestInit
): Promise<T> {
  const response = await fetch(resolveApiUrl(url), options)

  const payload = await readResponse(response)

  if (!response.ok) {
    throw new ApiError(response.status, payload)
  }

  return payload as T
}

function resolveApiUrl(url: string): string {
  if (typeof window !== "undefined") {
    return url
  }

  const backendUrl = (
    process.env.BACKEND_URL ?? DEFAULT_BACKEND_URL
  ).replace(/\/$/, "")

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
