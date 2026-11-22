import { PencilSimple } from '@phosphor-icons/react'
import { Link } from 'react-router'
import { useI18n } from '@/i18n/context'
import { cn } from '@/lib/utils'
import type { DerivedCorrection, FormCorrectionState } from '@/form/correction'
import type { BoundShape } from './Bound'
import { buttonClass, secondaryButtonClass } from './ui/button'

export function EditInputsLink({
  type,
  bound,
  derivedCorrection,
  primary,
}: {
  type: string
  bound?: BoundShape
  derivedCorrection?: DerivedCorrection
  primary: boolean
}) {
  const { t } = useI18n()
  const state: FormCorrectionState | undefined = derivedCorrection ? { derivedCorrection } : bound ? { bound } : undefined
  return (
    <Link
      to={`/calculations/new?type=${encodeURIComponent(type)}`}
      state={state}
      className={cn(buttonClass, !primary && secondaryButtonClass)}
    >
      <PencilSimple aria-hidden="true" size={18} />
      {t('result.edit')}
    </Link>
  )
}
