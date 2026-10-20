import type { FieldError } from '@/api/client'

export interface MappedErrors {
  byField: Record<string, string>
  general: string[]
}

export function mapFieldErrors(fields: readonly FieldError[], names: readonly string[]): MappedErrors {
  const byField: Record<string, string> = {}
  const general: string[] = []
  for (const { location, message } of fields) {
    const last = location[location.length - 1]
    if (typeof last === 'string' && names.includes(last)) {
      byField[last] ??= message
    } else {
      general.push(message)
    }
  }
  return { byField, general }
}
