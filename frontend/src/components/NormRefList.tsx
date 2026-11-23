import { useContext } from 'react'
import { CheckCircle, Warning } from '@phosphor-icons/react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { DemoResultDisplay } from '@/lib/resultDisplay'

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

function Part({ label, value, unconfirmed }: { label: string; value: string; unconfirmed: string }) {
  return (
    <span>
      {label}: {value === UNVERIFIED ? unconfirmed : value}
    </span>
  )
}

function groupReferences(refs: readonly NormRef[], compact: boolean): NormRef[][] {
  const groups: NormRef[][] = []
  const editions = new Map<string, NormRef[]>()
  for (const ref of refs) {
    if (compact && /^СП\s*22\.13330\.2016$/iu.test(ref.document.trim())) {
      const group = editions.get(ref.edition)
      if (group) {
        group.push(ref)
        continue
      }
      const entry = [ref]
      editions.set(ref.edition, entry)
      groups.push(entry)
    } else {
      groups.push([ref])
    }
  }
  return groups
}

export function NormRefList({ refs, showStatus = true }: { refs: readonly NormRef[]; showStatus?: boolean }) {
  const { t } = useI18n()
  const compact = useContext(DemoResultDisplay)
  return (
    <ul className="grid gap-1">
      {groupReferences(refs, compact).map((group, index) => {
        const [first] = group
        const sameStatus = group.every(({ status }) => status === first.status)
        const locators = [...new Map(group.map((ref) => [JSON.stringify([ref.clause, showStatus && ref.status]), ref])).values()]
        return (
          <li key={index} className="flex flex-wrap items-center gap-x-3 gap-y-1">
            <span className="font-medium">{first.document}</span>{' '}
            <Part label={t('norm.edition')} value={first.edition} unconfirmed={t('norm.editionUnconfirmed')} />{' '}
            {locators.length === 1 ? (
              <Part label={t('norm.clause')} value={first.clause} unconfirmed={t('norm.clauseUnconfirmed')} />
            ) : (
              <span className="min-w-0">
                {locators.map(({ clause, status }, i) => (
                  <span key={i}>
                    {i > 0 && '; '}{clause === UNVERIFIED ? t('norm.clauseUnconfirmed') : clause}
                    {showStatus && !sameStatus && <> <NormStatus status={status} /></>}
                  </span>
                ))}
              </span>
            )}
            {showStatus && sameStatus && <> {' '}<NormStatus status={first.status} /></>}
          </li>
        )
      })}
    </ul>
  )
}
