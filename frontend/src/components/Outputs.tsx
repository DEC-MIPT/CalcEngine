import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { unitLabel } from '@/i18n/units'
import { Source } from './Source'

type Output = components['schemas']['OutputValue']

function OutputItem({ output }: { output: Output }) {
  const { t, language, formatNumber } = useI18n()
  const { rounding_rule: rule } = output
  return (
    <li className="grid gap-3 border border-border bg-card p-4" data-output={output.quantity}>
      <h3 className="flex flex-wrap items-baseline gap-x-3">
        <code className="text-sm font-normal text-muted-foreground">{output.quantity}</code>
        <span className="text-2xl font-semibold">
          {formatNumber(output.value, rule.decimals)} {unitLabel(output.unit, language)}
        </span>
      </h3>
      <p>
        <span className="text-sm font-medium">{t('outputs.rounding')}: </span>
        {t(`outputs.mode.${rule.mode}`)}; {t('outputs.decimals')}: {rule.decimals}
      </p>
      <div>
        <h4 className="text-sm font-medium">{t('outputs.source')}</h4>
        <Source source={output.rounding_source} />
      </div>
    </li>
  )
}

export function Outputs({ outputs }: { outputs: readonly Output[] }) {
  const { t } = useI18n()
  return (
    <section aria-labelledby="outputs-title" className="mt-8 grid gap-4">
      <h2 id="outputs-title">{t('outputs.title')}</h2>
      <ul className="grid gap-3">
        {outputs.map((output) => (
          <OutputItem key={output.quantity} output={output} />
        ))}
      </ul>
    </section>
  )
}
