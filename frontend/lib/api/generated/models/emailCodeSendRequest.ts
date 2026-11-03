/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { EmailCodeSendRequestPurpose } from "./emailCodeSendRequestPurpose"

/**
 * 验证码发送请求。
 */
export interface EmailCodeSendRequest {
  /**
   * 邮箱
   * @maxLength 254
   */
  email: string
  purpose?: EmailCodeSendRequestPurpose
}
