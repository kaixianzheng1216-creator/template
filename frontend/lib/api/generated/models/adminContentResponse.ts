/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { ContentOwnerResponse } from "./contentOwnerResponse"

export interface AdminContentResponse {
  /** 内容 ID */
  id: string
  /** 内容标题 */
  title: string
  /** 内容描述 */
  description: string | null
  /** 创建时间 */
  created_at: string
  /** 所属用户 */
  owner: ContentOwnerResponse
}
