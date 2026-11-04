/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { UserProfileUpdateRequest, UserResponse } from "../../models"

import { apiFetch } from "../../../client"

export const getUsersGetCurrentUserUrl = () => {
  return `/api/v1/users/me`
}

/**
 * @summary 获取当前用户
 */
export const usersGetCurrentUser = async (
  options?: Parameters<typeof apiFetch>[1]
): Promise<UserResponse> => {
  return apiFetch<UserResponse>(getUsersGetCurrentUserUrl(), {
    ...options,
    method: "GET",
  })
}

export const getUsersUpdateCurrentUserUrl = () => {
  return `/api/v1/users/me`
}

/**
 * @summary 更新当前用户资料
 */
export const usersUpdateCurrentUser = async (
  userProfileUpdateRequest: UserProfileUpdateRequest,
  options?: Parameters<typeof apiFetch>[1]
): Promise<UserResponse> => {
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
  return apiFetch<UserResponse>(getUsersUpdateCurrentUserUrl(), {
    ...options,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(userProfileUpdateRequest),
  })
}
