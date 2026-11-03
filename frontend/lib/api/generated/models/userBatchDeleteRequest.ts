/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

/**
 * 用户批量删除请求。
 */
export interface UserBatchDeleteRequest {
  /**
   * @minItems 1
   * @maxItems 100
   */
  ids: string[]
}
