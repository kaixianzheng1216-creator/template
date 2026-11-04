/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type {
  UserBatchDeleteRequest,
  UserListResponse,
  UserProfileUpdateRequest,
  UserResponse,
  UserRoleUpdateRequest,
  UserStatusUpdateRequest,
  UsersListUsersParams,
} from "../../models"

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

export const getUsersListUsersUrl = (params?: UsersListUsersParams) => {
  const normalizedParams = new URLSearchParams()

  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined) {
      normalizedParams.append(key, value === null ? "null" : String(value))
    }
  })

  const stringifiedParams = normalizedParams.toString()

  return stringifiedParams.length > 0
    ? `/api/v1/users?${stringifiedParams}`
    : `/api/v1/users`
}

/**
 * @summary 分页查询用户（管理员）
 */
export const usersListUsers = async (
  params?: UsersListUsersParams,
  options?: Parameters<typeof apiFetch>[1]
): Promise<UserListResponse> => {
  return apiFetch<UserListResponse>(getUsersListUsersUrl(params), {
    ...options,
    method: "GET",
  })
}

export const getUsersUpdateUserRoleUrl = (userId: string) => {
  return `/api/v1/users/${userId}/role`
}

/**
 * @summary 更新用户角色（管理员）
 */
export const usersUpdateUserRole = async (
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
  return apiFetch<UserResponse>(getUsersUpdateUserRoleUrl(userId), {
    ...options,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(userRoleUpdateRequest),
  })
}

export const getUsersUpdateUserStatusUrl = (userId: string) => {
  return `/api/v1/users/${userId}/status`
}

/**
 * @summary 更新用户状态（管理员）
 */
export const usersUpdateUserStatus = async (
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
  return apiFetch<UserResponse>(getUsersUpdateUserStatusUrl(userId), {
    ...options,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(userStatusUpdateRequest),
  })
}

export const getUsersDeleteUsersUrl = () => {
  return `/api/v1/users/bulk-delete`
}

/**
 * @summary 批量删除用户及其内容（管理员）
 */
export const usersDeleteUsers = async (
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
  return apiFetch<void>(getUsersDeleteUsersUrl(), {
    ...options,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(options?.headers),
    },
    body: JSON.stringify(userBatchDeleteRequest),
  })
}
