/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

export interface PasswordLoginRequest {
  /**
   * 邮箱
   * @maxLength 254
   */
  email: string
  /**
   * 密码
   * @minLength 8
   * @maxLength 128
   */
  password: string
}
