import "client-only"

import { loginLoginAccessToken } from "@/lib/api/generated/endpoints"
import type { BodyLoginLoginAccessToken } from "@/lib/api/generated/models"
import { clearAccessToken, setAccessToken } from "@/lib/auth/token-storage"

export type LoginInput = Pick<
  BodyLoginLoginAccessToken,
  "username" | "password"
>
export async function login(input: LoginInput) {
  const token = await loginLoginAccessToken(input)

  setAccessToken(token.access_token)

  return token
}

export function logout(): void {
  clearAccessToken()
}
