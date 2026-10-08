import { Prohibit, WarningCircle } from '@phosphor-icons/react'
import { useId, type ReactNode } from 'react'
import { useI18n } from '@/i18n/context'
import { useFocusOnMount } from '@/lib/useFocusOnMount'

export type StatusTone = 'warning' | 'refusal'

const FRAMES: Record<StatusTone, string> = {
  warning: 'border-2 border-dashed border-warning bg-warning-surface',
  refusal: 'border-4 border-double border-destructive bg-destructive-surface',
}

const ICONS = { warning: WarningCircle, refusal: Prohibit } as const

export function Status({
  tone,
  title,
  children,
  focusOnMount = false,
}: {
  tone: StatusTone
  title: string
  children: ReactNode
  focusOnMount?: boolean
}) {
  const { t } = useI18n()
  const headingId = useId()
  const focus = useFocusOnMount<HTMLElement>(focusOnMount)
  const Icon = ICONS[tone]
  return (
    <section
      ref={focus}
      tabIndex={focusOnMount ? -1 : undefined}
      aria-labelledby={headingId}
      className={`${focusOnMount ? 'stamp-frame ' : ''}grid gap-3 p-4 ${FRAMES[tone]}`}
      data-status={tone}
    >
      <h2 id={headingId} className="flex items-start gap-x-2 text-lg">
        <Icon aria-hidden="true" weight="fill" size={22} className="mt-0.5 shrink-0" />
        <span>
          <span className="font-semibold">{t(`status.${tone}`)}:</span> <span className="font-normal">{title}</span>
        </span>
      </h2>
      {children}
    </section>
  )
}
