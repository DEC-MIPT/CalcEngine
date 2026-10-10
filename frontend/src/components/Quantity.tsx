import { useI18n } from '@/i18n/context'
import { unitLabel } from '@/i18n/units'

export function QuantityText({ value, unit, unitClassName }: { value: number; unit: string; unitClassName?: string }) {
  const { language, formatNumber } = useI18n()
  const label = unitLabel(unit, language)
  return (
    <>
      {formatNumber(value)}
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
