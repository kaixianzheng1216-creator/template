"use client"

import { useQuery } from "@tanstack/react-query"

import { usersReadUserMe } from "@/lib/api/generated/endpoints"

export const currentUserQueryKey = ["current-user"] as const

export function useCurrentUser() {
  return useQuery({
    queryKey: currentUserQueryKey,
    queryFn: () => usersReadUserMe(),
  })
}
