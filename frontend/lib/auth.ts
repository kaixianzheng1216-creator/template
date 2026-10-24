type SessionClaims = {
  metadata?: { role?: string }
}

export function hasAdminRole(claims: unknown): boolean {
  return (claims as SessionClaims | null)?.metadata?.role === "admin"
}
