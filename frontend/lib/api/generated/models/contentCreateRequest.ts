/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

/**
 * 内容创建请求。
 */
export interface ContentCreateRequest {
  /**
   * 内容标题
   * @minLength 1
   * @maxLength 255
   */
  title: string
  /** 内容描述 */
  description?: string | null
}
