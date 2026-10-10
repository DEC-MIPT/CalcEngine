import type { Language } from './dictionary'

const designations: Readonly<Record<string, string>> = {
  m: 'м',
  cm: 'см',
  mm: 'мм',
  m2: 'м²',
  N: 'Н',
  kN: 'кН',
  MN: 'МН',
  Pa: 'Па',
  kPa: 'кПа',
  MPa: 'МПа',
  'N/m3': 'Н/м³',
  'kN/m3': 'кН/м³',
  rad: 'рад',
  deg: '°',
}

export const DIMENSIONLESS = '1'

export function unitLabel(code: string, language: Language): string {
  if (code === DIMENSIONLESS) return ''
  return language === 'ru' ? (designations[code] ?? code) : code
}
