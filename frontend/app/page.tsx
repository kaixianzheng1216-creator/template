import { Button } from "@/components/ui/button"
import { InfrastructureStatus } from "@/components/infrastructure-status"

export default function Page() {
  return (
    <div className="flex min-h-svh p-6">
      <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
        <div>
          <h1 className="font-medium">初始化完成</h1>
          <p>Next.js 前端通过同源 API 代理连接 FastAPI 后端。</p>
          <InfrastructureStatus />
          <Button className="mt-2">开始使用</Button>
        </div>
        <div className="font-mono text-xs text-muted-foreground">
          （按 <kbd>d</kbd> 切换深色模式）
        </div>
      </div>
    </div>
  )
}
