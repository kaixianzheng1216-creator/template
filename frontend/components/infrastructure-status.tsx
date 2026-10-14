"use client"

import * as React from "react"

import { utilsHealthCheck } from "@/lib/api/generated/endpoints"

type Status = "checking" | "online" | "offline"

export function InfrastructureStatus() {
  const [status, setStatus] = React.useState<Status>("checking")

  React.useEffect(() => {
    const controller = new AbortController()

    utilsHealthCheck({
      signal: controller.signal,
    })
      .then((healthy) => setStatus(healthy ? "online" : "offline"))
      .catch(() => setStatus("offline"))

    return () => controller.abort()
  }, [])

  const labels: Record<Status, string> = {
    checking: "正在检查后端连接",
    online: "前后端连接正常",
    offline: "后端暂不可用",
  }

  return (
    <div className="flex items-center gap-2 text-sm text-muted-foreground">
      <span
        className="size-2 rounded-full bg-current"
        data-status={status}
        aria-hidden="true"
      />
      <span>{labels[status]}</span>
    </div>
  )
}
