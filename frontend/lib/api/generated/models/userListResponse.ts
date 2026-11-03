/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { UserResponse } from "./userResponse"

/**
 * 用户列表响应。
 */
export interface UserListResponse {
  /** 当前页数据 */
  data: UserResponse[]
  /** 记录总数 */
  count: number
}
