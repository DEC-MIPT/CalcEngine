import type { FieldError } from '@/api/client'

export interface ReportErrors {
  byField: Record<string, string>
  general: string[]
}

export function mapReportErrors(fields: readonly FieldError[], keys: readonly string[]): ReportErrors {
  const byField: Record<string, string> = {}
  const general: string[] = []
  for (const { location, message } of fields) {
    const key = location[0] === 'body' ? location.slice(1).join('.') : ''
    if (keys.includes(key)) {
      byField[key] ??= message
    } else {
      general.push(message)
    }
  }
  return { byField, general }
}
