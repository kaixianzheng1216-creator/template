/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { EmailCodeSendRequestPurpose } from "./emailCodeSendRequestPurpose"

export interface EmailCodeSendRequest {
  /**
   * 邮箱
   * @maxLength 254
   */
  email: string
  /** 验证码用途 */
  purpose?: EmailCodeSendRequestPurpose
}
