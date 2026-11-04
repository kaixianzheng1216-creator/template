/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

/**
 * 验证码用途
 */
export type EmailCodeSendRequestPurpose =
  (typeof EmailCodeSendRequestPurpose)[keyof typeof EmailCodeSendRequestPurpose]

export const EmailCodeSendRequestPurpose = {
  email_login: "email_login",
  password_reset: "password_reset",
} as const
