/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { ContentResponse } from "./contentResponse"

export interface ContentListResponse {
  /** 当前页数据 */
  data: ContentResponse[]
  /** 记录总数 */
  count: number
}
