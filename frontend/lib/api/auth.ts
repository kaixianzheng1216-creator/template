import "client-only"

import { loginLoginAccessToken } from "@/lib/api/generated/endpoints"
import type { BodyLoginLoginAccessToken } from "@/lib/api/generated/models"
import { clearAccessToken, setAccessToken } from "@/lib/auth/token-storage"

export async function login(
  input: Pick<BodyLoginLoginAccessToken, "username" | "password">
) {
  const token = await loginLoginAccessToken(input)

  setAccessToken(token.access_token)

  return token
}

export function logout(): void {
  clearAccessToken()
}
