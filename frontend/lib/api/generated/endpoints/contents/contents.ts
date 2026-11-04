/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type {
  ContentBatchDeleteRequest,
  ContentCreateRequest,
  ContentListResponse,
  ContentResponse,
  ContentUpdateRequest,
  ContentsListContentsParams,
} from "../../models"

import { apiFetch } from "../../../client"

export const getContentsListContentsUrl = (
  params?: ContentsListContentsParams
) => {
  const normalizedParams = new URLSearchParams()

  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined) {
      normalizedParams.append(key, value === null ? "null" : String(value))
    }
  })

  const stringifiedParams = normalizedParams.toString()

  return stringifiedParams.length > 0
    ? `/api/v1/contents?${stringifiedParams}`
    : `/api/v1/contents`
}

/**
 * @summary 分页查询我的内容
 */
export const contentsListContents = async (
  params?: ContentsListContentsParams,
  options?: Parameters<typeof apiFetch>[1]
): Promise<ContentListResponse> => {
  return apiFetch<ContentListResponse>(getContentsListContentsUrl(params), {
    ...options,
    method: "GET",
  })
}

export const getContentsCreateContentUrl = () => {
  return `/api/v1/contents`
}

/**
 * @summary 创建我的内容
 */
export const contentsCreateContent = async (
  contentCreateRequest: ContentCreateRequest,
  options?: Parameters<typeof apiFetch>[1]
): Promise<ContentResponse> => {
  const getHeaders = (
    h?: NonNullable<RequestInit["headers"]>
  ): Record<string, string | readonly string[]> => {
    if (!h) return {}
    if (h instanceof Headers) return Object.fromEntries(h.entries())
    if (Symbol.iterator in h) {
      return Object.fromEntries(
        Array.from(
          h as Iterable<Iterable<string>>,
          (entry) => Array.from(entry) as [string, string]
        )
      )
    }
    const headers: Record<string, string | readonly string[]> = {}
    for (const [name, value] of Object.entries<
      string | readonly string[] | undefined
    >(h)) {
      if (value !== undefined) headers[name] = value
    }
    return headers
  }
  return apiFetch<ContentResponse>(getContentsCreateContentUrl(), {
    ...options,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(contentCreateRequest),
  })
}

export const getContentsUpdateContentUrl = (contentId: string) => {
  return `/api/v1/contents/${contentId}`
}

/**
 * @summary 更新我的内容
 */
export const contentsUpdateContent = async (
  contentId: string,
  contentUpdateRequest: ContentUpdateRequest,
  options?: Parameters<typeof apiFetch>[1]
): Promise<ContentResponse> => {
  const getHeaders = (
    h?: NonNullable<RequestInit["headers"]>
  ): Record<string, string | readonly string[]> => {
    if (!h) return {}
    if (h instanceof Headers) return Object.fromEntries(h.entries())
    if (Symbol.iterator in h) {
      return Object.fromEntries(
        Array.from(
          h as Iterable<Iterable<string>>,
          (entry) => Array.from(entry) as [string, string]
        )
      )
    }
    const headers: Record<string, string | readonly string[]> = {}
    for (const [name, value] of Object.entries<
      string | readonly string[] | undefined
    >(h)) {
      if (value !== undefined) headers[name] = value
    }
    return headers
  }
  return apiFetch<ContentResponse>(getContentsUpdateContentUrl(contentId), {
    ...options,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(contentUpdateRequest),
  })
}

export const getContentsDeleteContentsUrl = () => {
  return `/api/v1/contents/bulk-delete`
}

/**
 * @summary 批量删除我的内容
 */
export const contentsDeleteContents = async (
  contentBatchDeleteRequest: ContentBatchDeleteRequest,
  options?: Parameters<typeof apiFetch>[1]
): Promise<void> => {
  const getHeaders = (
    h?: NonNullable<RequestInit["headers"]>
  ): Record<string, string | readonly string[]> => {
    if (!h) return {}
    if (h instanceof Headers) return Object.fromEntries(h.entries())
    if (Symbol.iterator in h) {
      return Object.fromEntries(
        Array.from(
          h as Iterable<Iterable<string>>,
          (entry) => Array.from(entry) as [string, string]
        )
      )
    }
    const headers: Record<string, string | readonly string[]> = {}
    for (const [name, value] of Object.entries<
      string | readonly string[] | undefined
    >(h)) {
      if (value !== undefined) headers[name] = value
    }
    return headers
  }
  return apiFetch<void>(getContentsDeleteContentsUrl(), {
    ...options,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(contentBatchDeleteRequest),
  })
}
