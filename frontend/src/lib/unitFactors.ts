export const UNIT_FACTORS: Readonly<Record<string, number>> = {
  '1': 1,
  m: 1,
  cm: 1e-2,
  mm: 1e-3,
  m2: 1,
  m3: 1,
  'N*m': 1,
  'kN*m': 1e3,
  'MN*m': 1e6,
  N: 1,
  kN: 1e3,
  MN: 1e6,
  Pa: 1,
  kPa: 1e3,
  MPa: 1e6,
  'N/m3': 1,
  'kN/m3': 1e3,
  rad: 1,
  deg: Math.PI / 180,
}

const SIGNIFICANT_DIGITS = 6

export function toBaseUnit(value: number, unit: string, base: string): number | null {
  if (!Object.hasOwn(UNIT_FACTORS, unit) || !Object.hasOwn(UNIT_FACTORS, base)) return null
  const converted = (value * UNIT_FACTORS[unit]) / UNIT_FACTORS[base]
  return Number.isFinite(converted) ? Number(converted.toPrecision(SIGNIFICANT_DIGITS)) : null
}
