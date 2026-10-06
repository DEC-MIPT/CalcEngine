import { CheckCircle, Warning } from '@phosphor-icons/react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'

type NormRef = components['schemas']['NormRef']

const UNVERIFIED = 'unverified'

export function NormStatus({ status }: { status: NormRef['status'] }) {
  const { t } = useI18n()
  const verified = status === 'verified'
  const Icon = verified ? CheckCircle : Warning
  return (
    <span
      className={
        verified
          ? 'inline-flex items-center gap-1 border border-success bg-success-surface px-1.5 text-sm text-success'
          : 'inline-flex items-center gap-1 border border-warning bg-warning-surface px-1.5 text-sm text-warning-foreground'
      }
    >
      <Icon aria-hidden="true" weight="fill" size={16} />
      {t(verified ? 'norm.verified' : 'norm.unverified')}
    </span>
  )
}

function Part({ label, value }: { label: string; value: string }) {
  const { t } = useI18n()
  return (
    <span>
      {label}: {value === UNVERIFIED ? t('norm.unverified') : value}
    </span>
  )
}

export function NormRefList({ refs }: { refs: readonly NormRef[] }) {
  const { t } = useI18n()
  return (
    <ul className="grid gap-1">
      {refs.map((ref, index) => (
        <li key={index} className="flex flex-wrap items-center gap-x-3 gap-y-1">
          <span className="font-medium">{ref.document}</span> <Part label={t('norm.edition')} value={ref.edition} />{' '}
          <Part label={t('norm.clause')} value={ref.clause} /> <NormStatus status={ref.status} />
        </li>
      ))}
    </ul>
  )
}
