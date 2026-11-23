import { useCallback } from 'react'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'
import { useRequest } from '@/api/useRequest'
import { useI18n } from '@/i18n/context'
import { QuantityText } from './Quantity'
import { ErrorState, LoadingState } from './RequestStates'

type Context = components['schemas']['FoundationContext']
type Quantities = Context['inputs']

const upperKeys = ['N', 'Mx', 'My', 'Qx', 'Qy', 'h']
const weights = ['G_fund', 'G_soil', 'G_other']
const baseKeys = ['Mx_add_base', 'My_add_base']
const resultantKeys = ['V', 'Mx_base', 'My_base']
const extrema = ['p', 'p_x_min', 'p_x_max', 'p_y_min', 'p_y_max', 'p_corner_min', 'p_corner_max']

function EvidenceValues({ keys, values }: { keys: readonly string[]; values: Quantities }) {
  return <dl className="grid grid-cols-[minmax(0,1fr)_auto] gap-x-3 gap-y-1 text-sm">
    {keys.map((key) => values[key] && (
      <div className="contents" key={key}>
        <dt className="break-words font-mono">{key}</dt>
        <dd><QuantityText {...values[key]} /></dd>
      </div>
    ))}
  </dl>
}

function LoadSchematic({ context }: { context: Context }) {
  const { t } = useI18n()
  const explicit = context.weight_mode === 'explicit'
  return <section aria-labelledby="foundation-evidence-title" className="grid min-w-0 gap-4">
    <h2 id="foundation-evidence-title">{t('foundation.schematic')}</h2>
    <p>{t(explicit ? 'foundation.explicit' : 'foundation.averaged')} · {t('foundation.upper')}</p>
    <div className="grid min-w-0 gap-5 md:grid-cols-[minmax(0,20rem)_minmax(0,1fr)]">
      <svg role="img" aria-labelledby="foundation-diagram-title" viewBox="0 0 320 180" className="block w-full max-w-[20rem] text-foreground">
        <title id="foundation-diagram-title">{t('foundation.schematic')}: {t('foundation.upper')}, {t('foundation.base')}</title>
        <g fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M32 60H235M32 139H235M106 60V129H48V139H219V129H160V60" />
          <path d="M133 18v37m-6-8 6 8 6-8M245 60h12m-6 0v79m-6 0h12M48 150v12m0-6h171m0-6v12" />
        </g>
        <g fill="currentColor" className="font-mono text-sm">
          <text x="145" y="30">N</text><text x="145" y="52">{t('foundation.upper')}</text>
          <text x="263" y="106">h</text><text x="114" y="174">b · x</text>
          <text x="39" y="104">{explicit ? 'G' : 'γ · d'}</text><text x="32" y="124">{t('foundation.base')}</text>
        </g>
      </svg>
      <div className="grid min-w-0 gap-3 border border-border p-3 sm:grid-cols-2">
        <div><h3>{t('foundation.upper')}</h3><EvidenceValues keys={upperKeys} values={context.inputs} /></div>
        <div><h3>{t('foundation.base')} · x=b, y=l</h3><EvidenceValues keys={['b', 'l', 'A']} values={context.geometry} />
          <EvidenceValues keys={explicit ? [...weights, ...baseKeys] : ['d']} values={context.inputs} />
          <EvidenceValues keys={explicit ? ['G_sum', ...resultantKeys] : ['gamma_mt', ...resultantKeys]} values={context.trace_values} />
        </div>
      </div>
    </div>
  </section>
}

function PressureEvidence({ context }: { context: Context }) {
  const { t } = useI18n()
  if (context.pressure_state === 'unavailable') return <p>{t('foundation.unavailable')}</p>
  const diagnostic = context.pressure_state === 'diagnostic'
  const maxMagnitude = Math.max(1, ...context.corners.map(({ pressure }) => Math.abs(pressure.value)))
  return <section aria-labelledby="foundation-pressure-title" className="grid min-w-0 gap-4">
    <h2 id="foundation-pressure-title">{t('foundation.pressures')}</h2>
    {diagnostic && <p className="border border-warning bg-warning-surface p-3">{t('foundation.diagnostic')}</p>}
    <div className="grid min-w-0 gap-4 md:grid-cols-[minmax(0,20rem)_minmax(0,1fr)]">
      <svg role="img" aria-label={t('foundation.corners')} viewBox="0 0 300 150" className="block w-full max-w-[20rem] text-foreground">
        <path d="M155 8v132" stroke="currentColor" /><text x="151" y="149" fill="currentColor" className="text-xs">0</text>
        {context.corners.map(({ name, pressure }, index) => {
          const y = 15 + 30 * index
          const dx = 105 * (pressure.value / maxMagnitude)
          return <g key={name} className="font-mono text-sm">
            <text x="8" y={y + 5} fill="currentColor">{name}</text>
            <path d={`M155 ${y}h${dx}`} stroke="currentColor" strokeWidth="6" strokeDasharray={pressure.value < 0 ? '4 2' : undefined} />
            <circle cx={155 + dx} cy={y} r="3" fill="currentColor" />
          </g>
        })}
      </svg>
      <div className="grid min-w-0 gap-3">
        <table className="w-full border-collapse border border-border text-sm">
          <caption className="sr-only">{t('foundation.corners')}</caption>
          <thead><tr><th scope="col" className="p-1 text-left">{t('foundation.corner')}</th><th scope="col">x</th><th scope="col">y</th><th scope="col">{t('foundation.pressureValue')}</th></tr></thead>
          <tbody>{context.corners.map((corner) => (
            <tr key={corner.name} data-pressure-step={corner.step_id} className="border-t border-border text-center">
              <th scope="row" className="p-1 text-left font-mono">{corner.name}</th>
              <td><QuantityText {...corner.x} /></td><td><QuantityText {...corner.y} /></td><td><QuantityText {...corner.pressure} /></td>
            </tr>
          ))}</tbody>
        </table>
        <EvidenceValues keys={extrema} values={context.trace_values} />
      </div>
    </div>
  </section>
}

export function FoundationEvidence({ resultId, inputHash }: { resultId: string; inputHash: string }) {
  const { t } = useI18n()
  const load = useCallback(() => unwrap(api.GET('/foundation-calculations/{result_id}/context', {
    params: { path: { result_id: resultId } },
  })), [resultId])
  const { state, retry } = useRequest(load)
  const unavailable = <p className="mt-6 text-sm">{t('foundation.unavailable')}</p>
  if (state.status === 'loading') return <div className="mt-6"><LoadingState /></div>
  if (state.status === 'error') return state.error.kind === 'api' && state.error.code === 'foundation_context_unavailable' ? unavailable : (
    <div className="mt-6"><ErrorState error={state.error} onRetry={retry} title="foundation.contextError" /></div>
  )
  const context = state.data.context
  if (state.data.status !== 'available' || !context || context.result_id !== resultId || context.input_hash !== inputHash) return unavailable
  return <div className="mt-8 grid min-w-0 gap-8"><LoadSchematic context={context} /><PressureEvidence context={context} /></div>
}
