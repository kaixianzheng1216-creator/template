import "client-only"

import { ApiError } from "@/lib/api/client"
import {
  loginLoginAccessToken,
  usersReadUserMe,
  usersRegisterUser,
} from "@/lib/api/generated/endpoints"
import type {
  BodyLoginLoginAccessToken,
  Token,
  UserPublic,
  UserRegister,
} from "@/lib/api/generated/models"
import {
  clearAccessToken,
  getAccessToken,
  setAccessToken,
} from "@/lib/auth/token-storage"

const AUTHENTICATION_ERROR_STATUS = {
  unauthorized: 401,
  forbidden: 403,
} as const

const AUTHENTICATION_ERROR_STATUSES = new Set<number>(
  Object.values(AUTHENTICATION_ERROR_STATUS)
)

export type LoginInput = Pick<
  BodyLoginLoginAccessToken,
  "username" | "password"
>
export type RegisterInput = UserRegister

export async function login(input: LoginInput): Promise<Token> {
  const token = await loginLoginAccessToken(input)

  setAccessToken(token.access_token)

  return token
}

export function logout(): void {
  clearAccessToken()
}

export async function getCurrentUser(): Promise<UserPublic> {
  try {
    const user = await usersReadUserMe(getAuthenticatedRequestOptions())

    return user
  } catch (error) {
    clearInvalidAccessToken(error)

    throw error
  }
}

export function register(input: RegisterInput): Promise<UserPublic> {
  return usersRegisterUser(input)
}

function getAuthenticatedRequestOptions(): RequestInit {
  const accessToken = getAccessToken()

  if (!accessToken) {
    return {}
  }

  return {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  }
}

function clearInvalidAccessToken(error: unknown): void {
  if (
    error instanceof ApiError &&
    AUTHENTICATION_ERROR_STATUSES.has(error.status)
  ) {
    clearAccessToken()
  }
}
