import type { components } from '@/api/schema'
import type { CandidateDraft } from '@/form/draftContext'
import { candidateFieldId } from '@/form/foundationCandidates'
import { useEffect, useRef } from 'react'
import { useI18n } from '@/i18n/context'
import { unitLabel } from '@/i18n/units'
import { CANDIDATE_LIMIT } from '@/lib/foundationDesign'
import { Button } from './ui/button'

type Input = components['schemas']['InputView']
const axes = ['b', 'l'] as const
export function CandidateFields({ candidates, dimensions, errors, locked, onChange }: {
  candidates: readonly CandidateDraft[]
  dimensions: readonly Input[]
  errors: Record<string, string>
  locked: boolean
  onChange: (rows: readonly CandidateDraft[]) => void
}) {
  const { t, language } = useI18n()
  const focusAfterRemove = useRef<string | null>(null)
  useEffect(() => {
    if (!focusAfterRemove.current) return
    document.getElementById(focusAfterRemove.current)?.focus()
    focusAfterRemove.current = null
  }, [candidates])
  function update(row: CandidateDraft, patch: Partial<CandidateDraft>) {
    onChange(candidates.map((item) => item.id === row.id ? { ...item, ...patch } : item))
  }
  return (
    <fieldset disabled={locked} className="grid min-w-0 grid-cols-[minmax(0,1fr)] [min-inline-size:0] gap-3 border border-border p-3">
      <legend className="font-heading text-xl">{t('foundation.candidates')}</legend>
      {candidates.map((row, index) => (
        <fieldset key={row.id} className="grid min-w-0 grid-cols-[minmax(0,1fr)] [min-inline-size:0] gap-3 border-b border-border pb-3 sm:grid-cols-[minmax(0,1fr)_minmax(0,1fr)_auto]">
          <legend className="mb-2 font-medium">{t('foundation.candidate')} {index + 1}</legend>
          {axes.map((axis) => {
            const id = candidateFieldId(`${row.id}-${axis}`)
            const error = errors[`${row.id}-${axis}`]
            const units = dimensions.find((dimension) => dimension.name === axis)?.units ?? ['m']
            return (
              <div key={axis} className="grid min-w-0 grid-cols-[minmax(0,1fr)] gap-1">
                <label htmlFor={id}>{axis} · {t('foundation.candidate')} {index + 1}</label>
                <div className="flex gap-2">
                  <input id={id} type="text" inputMode="decimal" autoComplete="off" value={row[axis]}
                    aria-invalid={!!error} aria-describedby={error ? `${id}-error` : undefined}
                    onChange={(event) => update(row, { [axis]: event.target.value })}
                    className="w-0 min-w-0 flex-1 border border-input bg-card px-2 py-1.5 font-mono" />
                  <select aria-label={`${t('form.unit')} ${axis} · ${t('foundation.candidate')} ${index + 1}`}
                    value={row[`${axis}Unit`]} className="border border-input bg-card px-2"
                    onChange={(event) => update(row, { [`${axis}Unit`]: event.target.value })}>
                    {units.map((unit) => <option key={unit} value={unit}>{unitLabel(unit, language)}</option>)}
                  </select>
                </div>
                {error && <p id={`${id}-error`} className="text-sm text-destructive">{error}</p>}
              </div>
            )
          })}
          <Button type="button" disabled={candidates.length === 1} className="self-end"
            aria-label={`${t('foundation.remove')} ${index + 1}`}
            onClick={() => {
              const position = candidates.findIndex((item) => item.id === row.id)
              const next = candidates[position + 1] ?? candidates[position - 1]
              if (next) focusAfterRemove.current = candidateFieldId(`${next.id}-b`)
              onChange(candidates.filter((item) => item.id !== row.id))
            }}>{t('foundation.remove')}</Button>
        </fieldset>
      ))}
      <Button type="button" disabled={candidates.length >= CANDIDATE_LIMIT} className="justify-self-start"
        onClick={() => {
          const id = (candidates.at(-1)?.id ?? -1) + 1
          onChange([...candidates, { id, b: '', l: '', bUnit: 'm', lUnit: 'm' }])
        }}>{t('foundation.add')}</Button>
    </fieldset>
  )
}
