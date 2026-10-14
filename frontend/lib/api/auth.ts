import "client-only"

import { apiFetch } from "@/lib/api/client"
import type {
  LoginInput,
  RegisterInput,
  Token,
  UserPublic,
} from "@/lib/api/types"
import { clearAccessToken, setAccessToken } from "@/lib/auth/token-storage"

export async function login(input: LoginInput): Promise<Token> {
  const body = new URLSearchParams({
    username: input.username,
    password: input.password,
  })

  const token = await apiFetch<Token>("/login/access-token", {
    method: "POST",
    auth: false,
    body,
  })

  setAccessToken(token.access_token)
  return token
}

export function logout(): void {
  clearAccessToken()
}

export function getCurrentUser(): Promise<UserPublic> {
  return apiFetch<UserPublic>("/users/me")
}

export function register(input: RegisterInput): Promise<UserPublic> {
  return apiFetch<UserPublic>("/users/signup", {
    method: "POST",
    auth: false,
    body: input,
  })
}
