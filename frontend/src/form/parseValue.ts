export type ParseError = 'empty' | 'notNumber' | 'notFinite' | 'notWhole'

export type Parsed = { ok: true; value: number } | { ok: false; error: ParseError }

const NUMBER = /^[+-]?(\d+([.,]\d*)?|[.,]\d+)([eE][+-]?\d+)?$/

export function parseValue(text: string, wholeOnly: boolean): Parsed {
  const trimmed = text.trim()
  if (trimmed === '') return { ok: false, error: 'empty' }
  if (!NUMBER.test(trimmed)) return { ok: false, error: 'notNumber' }
  const value = Number(trimmed.replace(',', '.'))
  if (!Number.isFinite(value)) return { ok: false, error: 'notFinite' }
  if (wholeOnly && !Number.isInteger(value)) return { ok: false, error: 'notWhole' }
  return { ok: true, value }
}
