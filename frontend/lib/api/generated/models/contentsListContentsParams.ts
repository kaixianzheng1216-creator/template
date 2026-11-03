/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { ContentsListContentsOrder } from "./contentsListContentsOrder"
import type { ContentsListContentsSort } from "./contentsListContentsSort"

export type ContentsListContentsParams = {
  /**
   * 跳过记录数
   * @minimum 0
   * @maximum 9223372036854776000
   */
  skip?: number
  /**
   * 最多返回记录数
   * @minimum 1
   * @maximum 100
   */
  limit?: number
  /** 排序方向 */
  order?: ContentsListContentsOrder
  /**
   * 按标题或描述搜索
   * @maxLength 255
   */
  search?: string
  /** 创建时间下限 */
  created_after?: string | null
  sort?: ContentsListContentsSort
}
