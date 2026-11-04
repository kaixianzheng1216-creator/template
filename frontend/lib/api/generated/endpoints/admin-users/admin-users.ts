/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type {
  AdminUserListResponse,
  AdminUsersListAdminUsersParams,
  UserBatchDeleteRequest,
  UserResponse,
  UserRoleUpdateRequest,
  UserStatusUpdateRequest,
} from "../../models"

import { apiFetch } from "../../../client"

export const getAdminUsersListAdminUsersUrl = (
  params?: AdminUsersListAdminUsersParams
) => {
  const normalizedParams = new URLSearchParams()

  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined) {
      normalizedParams.append(key, value === null ? "null" : String(value))
    }
  })

  const stringifiedParams = normalizedParams.toString()

  return stringifiedParams.length > 0
    ? `/api/v1/admin/users?${stringifiedParams}`
    : `/api/v1/admin/users`
}

/**
 * @summary 分页查询用户（管理员）
 */
export const adminUsersListAdminUsers = async (
  params?: AdminUsersListAdminUsersParams,
  options?: Parameters<typeof apiFetch>[1]
): Promise<AdminUserListResponse> => {
  return apiFetch<AdminUserListResponse>(
    getAdminUsersListAdminUsersUrl(params),
    {
      ...options,
      method: "GET",
    }
  )
}

export const getAdminUsersUpdateAdminUserRoleUrl = (userId: string) => {
  return `/api/v1/admin/users/${userId}/role`
}

/**
 * @summary 更新用户角色（管理员）
 */
export const adminUsersUpdateAdminUserRole = async (
  userId: string,
  userRoleUpdateRequest: UserRoleUpdateRequest,
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
  return apiFetch<UserResponse>(getAdminUsersUpdateAdminUserRoleUrl(userId), {
    ...options,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(userRoleUpdateRequest),
  })
}

export const getAdminUsersUpdateAdminUserStatusUrl = (userId: string) => {
  return `/api/v1/admin/users/${userId}/status`
}

/**
 * @summary 更新用户状态（管理员）
 */
export const adminUsersUpdateAdminUserStatus = async (
  userId: string,
  userStatusUpdateRequest: UserStatusUpdateRequest,
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
  return apiFetch<UserResponse>(getAdminUsersUpdateAdminUserStatusUrl(userId), {
    ...options,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(userStatusUpdateRequest),
  })
}

export const getAdminUsersDeleteAdminUsersUrl = () => {
  return `/api/v1/admin/users/bulk-delete`
}

/**
 * @summary 批量删除用户及其内容（管理员）
 */
export const adminUsersDeleteAdminUsers = async (
  userBatchDeleteRequest: UserBatchDeleteRequest,
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
  return apiFetch<void>(getAdminUsersDeleteAdminUsersUrl(), {
    ...options,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(userBatchDeleteRequest),
  })
}
