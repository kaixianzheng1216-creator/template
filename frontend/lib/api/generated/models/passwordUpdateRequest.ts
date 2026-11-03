/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

/**
 * 密码更新请求。
 */
export interface PasswordUpdateRequest {
  /** @pattern ^[0-9]{6}$ */
  code: string
  /**
   * @minLength 8
   * @maxLength 128
   */
  password: string
}
