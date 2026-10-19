import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { unitLabel } from '@/i18n/units'
import { roundValue } from '@/lib/rounding'

type RoundingRule = components['schemas']['RoundingRule']

export function QuantityText({
  value,
  unit,
  unitClassName,
  rounding,
}: {
  value: number
  unit: string
  unitClassName?: string
  rounding?: RoundingRule
}) {
  const { language, formatNumber } = useI18n()
  const label = unitLabel(unit, language)
  return (
    <>
      {rounding ? formatNumber(roundValue(value, rounding), rounding.decimals) : formatNumber(value)}
      {label && <> {unitClassName ? <span className={unitClassName}>{label}</span> : label}</>}
    </>
  )
}

export function UnitText({ unit }: { unit: string }) {
  const { t, language } = useI18n()
  const label = unitLabel(unit, language)
  if (label) return <>{label}</>
  return (
    <>
      <span aria-hidden="true">—</span>
      <span className="sr-only">{t('unit.dimensionless')}</span>
    </>
  )
}
