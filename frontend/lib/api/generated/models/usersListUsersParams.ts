/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { UsersListUsersOrder } from "./usersListUsersOrder"
import type { UsersListUsersSort } from "./usersListUsersSort"

export type UsersListUsersParams = {
  /**
   * 跳过记录数
   * @minimum 0
   * @maximum 9223372036854776000
   */
  skip?: number
  /**
   * 最多返回记录数
   * @minimum 1
   * @maximum 100
   */
  limit?: number
  /** 排序方向 */
  order?: UsersListUsersOrder
  /**
   * 按邮箱或昵称搜索
   * @maxLength 255
   */
  search?: string
  /** 是否启用 */
  is_active?: boolean | null
  sort?: UsersListUsersSort
}
