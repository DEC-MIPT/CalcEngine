import { PencilSimple } from '@phosphor-icons/react'
import { Link } from 'react-router'
import { useI18n } from '@/i18n/context'
import { cn } from '@/lib/utils'
import type { BoundShape } from './Bound'
import { buttonClass, secondaryButtonClass } from './ui/button'

export function EditInputsLink({
  type,
  bound,
  primary,
}: {
  type: string
  bound?: BoundShape
  primary: boolean
}) {
  const { t } = useI18n()
  return (
    <Link
      to={`/calculations/new?type=${encodeURIComponent(type)}`}
      state={bound ? { bound } : undefined}
      className={cn(buttonClass, !primary && secondaryButtonClass)}
    >
      <PencilSimple aria-hidden="true" size={18} />
      {t('result.edit')}
    </Link>
  )
}
