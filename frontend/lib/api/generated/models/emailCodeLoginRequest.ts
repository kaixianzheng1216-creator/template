/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

/**
 * 验证码登录请求。
 */
export interface EmailCodeLoginRequest {
  /**
   * 邮箱
   * @maxLength 254
   */
  email: string
  /** @pattern ^[0-9]{6}$ */
  code: string
}
