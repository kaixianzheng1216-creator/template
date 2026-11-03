/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

/**
 * 内容批量删除请求。
 */
export interface ContentBatchDeleteRequest {
  /**
   * 待删除内容 ID
   * @minItems 1
   * @maxItems 100
   */
  ids: string[]
}
