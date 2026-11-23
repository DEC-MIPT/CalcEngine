import { UserCheck } from '@phosphor-icons/react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { NormRefList } from './NormRefList'

type NormRef = components['schemas']['NormRef']
type EngineerRule = components['schemas']['EngineerRule']

export function Source({ source, omitEngineerName = false }: { source: readonly NormRef[] | EngineerRule; omitEngineerName?: boolean }) {
  const { t } = useI18n()
  if (Array.isArray(source)) {
    return <NormRefList refs={source} />
  }
  const rule = source as EngineerRule
  return (
    <div className="grid gap-1">
      <span className="inline-flex w-fit items-center gap-1 border border-border bg-secondary px-1.5 text-sm">
        <UserCheck aria-hidden="true" size={16} />
        {t('source.engineerSet')}
      </span>
      {!omitEngineerName && <p>{t('source.engineer')}: {rule.engineer}</p>}
      <p>
        {t('source.rationale')}: {rule.rationale}
      </p>
    </div>
  )
}
