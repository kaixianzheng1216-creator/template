import { format } from "date-fns"

export function formatDateTime(value: string): string {
  return format(new Date(value), "yyyy年M月d日 HH:mm")
}
