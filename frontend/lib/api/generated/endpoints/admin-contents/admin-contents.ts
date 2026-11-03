/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type {
  AdminContentListResponse,
  AdminContentsListAllContentsParams,
  ContentBatchDeleteRequest,
  ContentResponse,
  ContentUpdateRequest,
} from "../../models"

import { apiFetch } from "../../../client"

export const getAdminContentsListAllContentsUrl = (
  params?: AdminContentsListAllContentsParams
) => {
  const normalizedParams = new URLSearchParams()

  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined) {
      normalizedParams.append(key, value === null ? "null" : String(value))
    }
  })

  const stringifiedParams = normalizedParams.toString()

  return stringifiedParams.length > 0
    ? `/api/v1/admin/contents?${stringifiedParams}`
    : `/api/v1/admin/contents`
}

/**
 * @summary 分页查询全部内容
 */
export const adminContentsListAllContents = async (
  params?: AdminContentsListAllContentsParams,
  options?: Parameters<typeof apiFetch>[1]
): Promise<AdminContentListResponse> => {
  return apiFetch<AdminContentListResponse>(
    getAdminContentsListAllContentsUrl(params),
    {
      ...options,
      method: "GET",
    }
  )
}

export const getAdminContentsUpdateAnyContentUrl = (contentId: string) => {
  return `/api/v1/admin/contents/${contentId}`
}

/**
 * @summary 更新任意内容
 */
export const adminContentsUpdateAnyContent = async (
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
  return apiFetch<ContentResponse>(
    getAdminContentsUpdateAnyContentUrl(contentId),
    {
      ...options,
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...getHeaders(options?.headers),
      },
      body: JSON.stringify(contentUpdateRequest),
    }
  )
}

export const getAdminContentsDeleteAnyContentsUrl = () => {
  return `/api/v1/admin/contents/bulk-delete`
}

/**
 * @summary 批量删除任意内容
 */
export const adminContentsDeleteAnyContents = async (
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
  return apiFetch<void>(getAdminContentsDeleteAnyContentsUrl(), {
    ...options,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(contentBatchDeleteRequest),
  })
}
