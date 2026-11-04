/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */

export interface UserResponse {
  /** 用户 ID */
  id: string
  /** 邮箱 */
  email: string
  /** 是否已设置密码 */
  has_password: boolean
  /** 昵称 */
  name: string
  /** 头像地址 */
  avatar_url: string
  /** 是否为管理员 */
  is_admin: boolean
  /** 是否启用 */
  is_active: boolean
  /** 创建时间 */
  created_at: string
}
