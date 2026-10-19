import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { Checking } from './Checking'
import { UnitText } from './Quantity'
import { Source } from './Source'
import type { StampReveal } from './VerdictStamp'

type Output = components['schemas']['OutputValue']

const headCell = 'px-3 py-2 text-left text-sm font-medium text-muted-foreground'
const detailCell = 'px-3 py-3 text-sm max-sm:col-span-full max-sm:p-0'
const mobileLabel = 'text-sm font-medium sm:hidden'

function OutputRow({ output, source }: { output: Output; source: boolean }) {
  const { t, formatNumber } = useI18n()
  const { rounding_rule: rule } = output
  return (
    <tr
      data-output={output.quantity}
      className="data-row align-baseline not-last:border-b not-last:border-border max-sm:grid max-sm:grid-cols-[auto_auto_1fr] max-sm:items-baseline max-sm:gap-x-3 max-sm:gap-y-2 max-sm:p-3"
    >
      <th scope="row" className="px-3 py-3 text-left font-normal max-sm:p-0">
        <code className="text-lg">{output.quantity}</code>
      </th>
      <td className="px-3 py-3 text-right font-mono text-3xl font-semibold whitespace-nowrap max-sm:p-0" data-value>
        {formatNumber(output.value, rule.decimals)}
      </td>
      <td className="px-3 py-3 text-lg text-muted-foreground max-sm:p-0"><UnitText unit={output.unit} /></td>
      <td className={detailCell} data-rounding>
        <span className={mobileLabel}>{t('outputs.rounding')}: </span>
        {t(`outputs.mode.${rule.mode}`)}; {t('outputs.decimals')}: <span className="font-mono">{rule.decimals}</span>
      </td>
      {source && (
        <td className={detailCell} data-source>
          <span className={mobileLabel}>{t('outputs.source')}</span>
          <Source source={output.rounding_source} />
        </td>
      )}
    </tr>
  )
}

const REVEAL_CLASS: Record<StampReveal, string> = {
  pending: ' outputs-pending',
  celebrate: ' outputs-celebrate',
  plain: '',
  none: '',
}

export function Outputs({
  outputs,
  reveal = 'none',
  source = true,
}: {
  outputs: readonly Output[]
  reveal?: StampReveal
  source?: boolean
}) {
  const { t } = useI18n()
  return (
    <section aria-labelledby="outputs-title" className={`mt-8 grid gap-3${REVEAL_CLASS[reveal]}`} data-reveal={reveal}>
      <h2 id="outputs-title">{t('outputs.title')}</h2>
      <div className="relative">
        {reveal === 'pending' && <Checking marker="outputs" />}
        <table className="w-full border-collapse border border-border bg-card max-sm:block">
          <thead className="border-b border-foreground max-sm:hidden">
            <tr>
              <th scope="col" className={`${headCell} w-24`}>
                {t('outputs.column.quantity')}
              </th>
              <th scope="col" className={`${headCell} w-36 text-right`}>
                {t('outputs.column.value')}
              </th>
              <th scope="col" className={`${headCell} w-20`}>
                {t('outputs.column.unit')}
              </th>
              <th scope="col" className={source ? `${headCell} w-64` : headCell}>
                {t('outputs.rounding')}
              </th>
              {source && (
                <th scope="col" className={headCell}>
                  {t('outputs.source')}
                </th>
              )}
            </tr>
          </thead>
          <tbody className="max-sm:block" inert={reveal === 'pending'}>
            {outputs.map((output) => (
              <OutputRow key={output.quantity} output={output} source={source} />
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
