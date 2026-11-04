/**
 * 由 orval 自动生成
 * 请勿手动编辑。
 * 项目模板
 * OpenAPI 规范版本： 0.1.0
 */
import type { ValidationErrorDetailResponse } from "./validationErrorDetailResponse"

export interface ErrorResponse {
  /** 错误代码 */
  code: string
  /** 错误提示 */
  message: string
  /** 参数校验错误详情 */
  details?: ValidationErrorDetailResponse[] | null
}
