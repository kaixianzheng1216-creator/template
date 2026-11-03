/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { ValidationErrorDetail } from "./validationErrorDetail"

/**
 * 统一错误响应。
 */
export interface ErrorResponse {
  code: string
  message: string
  details?: ValidationErrorDetail[] | null
}
