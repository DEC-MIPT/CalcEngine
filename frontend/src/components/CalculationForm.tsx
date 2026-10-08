import { CaretDown, WarningCircle } from '@phosphor-icons/react'
import { useEffect, useRef, useState, type ChangeEvent, type CSSProperties, type FormEvent } from 'react'
import { useLocation, useNavigate } from 'react-router'
import { api, unwrap, type ApiError } from '@/api/client'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import type { TextKey } from '@/i18n/dictionary'
import { pickText } from '@/i18n/translate'
import { unitLabel } from '@/i18n/units'
import { prefersReducedMotion, withMinimumDuration } from '@/lib/motion'
import { toBaseUnit } from '@/lib/unitFactors'
import { parseValue, type ParseError } from '@/form/parseValue'
import { useDraft } from '@/form/draftContext'
import { mapFieldErrors } from '@/form/serverErrors'
import { useSendingHints, type SendingStage } from '@/form/useSendingHints'
import { BoundNote, type BoundShape } from './Bound'
import { ErrorState } from './RequestStates'
import { ComputePlot } from './ComputePlot'
import { Formula } from './Formula'
import { Button } from './ui/button'

type CalculationType = components['schemas']['CalculationTypeView']
type Input = CalculationType['inputs'][number]
type Quantity = components['schemas']['QuantityValue']

const parseErrorKey = {
  empty: 'form.error.empty',
  notNumber: 'form.error.notNumber',
  notFinite: 'form.error.notFinite',
  notWhole: 'form.error.notWhole',
} as const satisfies Record<ParseError, TextKey>

const stageText = {
  sending: 'form.sending',
  slow: 'form.sendingSlow',
  longer: 'form.sendingLonger',
} as const satisfies Record<SendingStage, TextKey>

const COMPUTE_MS = 700

const fieldId = (name: string) => `field-${name}`

const row = 'grid grid-cols-[2.5rem_minmax(0,1fr)] gap-x-3 gap-y-1.5 sm:grid-cols-[3.5rem_minmax(0,1fr)_15.5rem] sm:items-center'

function FieldMessage({ id, children }: { id: string; children: string }) {
  return (
    <p id={id} className="flex items-start gap-1.5 text-sm text-destructive">
      <WarningCircle aria-hidden="true" weight="fill" size={16} className="mt-0.5 shrink-0" />
      {children}
    </p>
  )
}

interface FieldProps {
  input: Input
  value: string
  unit: string
  error: string | undefined
  bound: BoundShape | undefined
  locked: boolean
  index: number
  onValue: (event: ChangeEvent<HTMLInputElement>) => void
  onUnit: (event: ChangeEvent<HTMLSelectElement>) => void
}

function Field({ input, value, unit, error, bound, locked, index, onValue, onUnit }: FieldProps) {
  const { t, language, formatNumber } = useI18n()
  const [flashing, setFlashing] = useState(false)
  const label = pickText(input.label, language)
  const hint = input.hint ? pickText(input.hint, language) : null
  const hintId = `hint-${input.name}`
  const errorId = `error-${input.name}`
  const noteId = `bound-${input.name}`
  const fixedUnit = input.whole_values_only || input.units.length === 1
  const echoId = `echo-${input.name}`
  const parsed = parseValue(value, false)
  const inBase = !fixedUnit && unit !== input.base_unit && parsed.ok ? toBaseUnit(parsed.value, unit, input.base_unit) : null
  const describedBy = [hint ? hintId : null, error ? errorId : null, bound ? noteId : null, inBase !== null ? echoId : null]
    .filter(Boolean)
    .join(' ')
  return (
    <div data-row style={{ '--row': index } as CSSProperties} className={`${row} border-b border-border py-2.5`}>
      <span
        aria-hidden="true"
        className={`row-span-2 pt-0.5 text-lg sm:row-span-1 sm:pt-0 ${error ? 'text-destructive' : ''}`}
      >
        <Formula latex={input.symbol} />
      </span>
      <div className="grid gap-0.5">
        <label htmlFor={fieldId(input.name)} className="font-medium">
          {label}
        </label>
        {hint && (
          <p id={hintId} className="text-xs text-muted-foreground">
            {hint}
          </p>
        )}
      </div>
      <div className="flex gap-2">
        <input
          id={fieldId(input.name)}
          name={input.name}
          type="text"
          inputMode="decimal"
          autoComplete="off"
          value={value}
          onChange={onValue}
          readOnly={locked}
          onAnimationEnd={() => setFlashing(false)}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy || undefined}
          className={`min-h-9 w-36 min-w-0 border ${bound && !error ? 'border-warning' : 'border-input'} bg-card px-2.5 py-1.5 text-right font-mono ${flashing ? 'unit-flash' : ''} read-only:bg-secondary focus-visible:outline-offset-[-1px] aria-invalid:border-destructive aria-invalid:focus-visible:outline-destructive`}
        />
        {fixedUnit ? (
          <span className="flex min-h-9 w-24 shrink-0 items-center px-2.5">{unitLabel(input.base_unit, language)}</span>
        ) : (
          <span className="relative w-24 shrink-0">
            <select
              value={unit}
              disabled={locked}
              onChange={(event) => {
                setFlashing(true)
                onUnit(event)
              }}
              aria-label={`${t('form.unit')}: ${label}`}
              className="min-h-9 w-full cursor-pointer appearance-none border border-input bg-card py-1.5 pr-7 pl-2.5 disabled:cursor-default disabled:bg-secondary focus-visible:outline-offset-[-1px]"
            >
              {input.units.map((code) => (
                <option key={code} value={code}>
                  {unitLabel(code, language)}
                </option>
              ))}
            </select>
            <CaretDown
              aria-hidden="true"
              size={14}
              className="pointer-events-none absolute top-1/2 right-2.5 -translate-y-1/2"
            />
          </span>
        )}
      </div>
      {(error || (bound && !error) || inBase !== null) && (
        <div className="col-start-2 grid gap-1 sm:col-start-3">
          {error && <FieldMessage id={errorId}>{error}</FieldMessage>}
          {bound && !error && <BoundNote id={noteId} bound={bound} unit={input.base_unit} />}
          {inBase !== null && (
            <p id={echoId} className="font-mono text-sm text-muted-foreground">
              = {formatNumber(inBase)} {unitLabel(input.base_unit, language)}
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export function CalculationForm({ type }: { type: CalculationType }) {
  const { t } = useI18n()
  const navigate = useNavigate()
  const draft = useDraft()
  const { values, units } = draft.read(type.name)
  const location = useLocation()
  const [bound, setBound] = useState<BoundShape | null>(
    () => (location.state as { bound?: BoundShape } | null)?.bound ?? null,
  )
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [general, setGeneral] = useState<string[]>([])
  const [failure, setFailure] = useState<ApiError | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [computing, setComputing] = useState(false)
  const inFlight = useRef(false)
  const stage = useSendingHints(submitting)

  async function send() {
    if (inFlight.current) return
    const inputs: Record<string, Quantity> = {}
    const invalid: Record<string, string> = {}
    for (const input of type.inputs) {
      const parsed = parseValue(values[input.name] ?? '', input.whole_values_only)
      if (parsed.ok) {
        inputs[input.name] = { value: parsed.value, unit: units[input.name] ?? input.base_unit }
      } else {
        invalid[input.name] = t(parseErrorKey[parsed.error])
      }
    }
    setErrors(invalid)
    setGeneral([])
    setFailure(null)
    const first = type.inputs.find((input) => input.name in invalid)
    if (first) {
      document.getElementById(fieldId(first.name))?.focus()
      return
    }

    inFlight.current = true
    const animated = !prefersReducedMotion()
    setComputing(animated)
    setSubmitting(true)
    const result = await withMinimumDuration(
      unwrap(api.POST('/calculations', { body: { calculation_type: type.name, inputs } })),
      animated ? COMPUTE_MS : 0,
    )
    setComputing(false)
    inFlight.current = false
    setSubmitting(false)
    if (result.ok) {
      draft.remember(result.data.result_id, type.name)
      void navigate(`/calculations/${result.data.result_id}`)
    } else if (result.error.kind === 'api' && result.error.status === 422) {
      const mapped = mapFieldErrors(
        result.error.fields,
        type.inputs.map((input) => input.name),
      )
      setErrors(mapped.byField)
      setGeneral(
        mapped.general.length === 0 && Object.keys(mapped.byField).length === 0
          ? [result.error.message]
          : mapped.general,
      )
    } else {
      setFailure(result.error)
    }
  }

  function submit(event: FormEvent) {
    event.preventDefault()
    void send()
  }

  useEffect(() => {
    if (bound) document.getElementById(fieldId(bound.quantity))?.focus()
  }, [bound])

  function change(name: string, text: string) {
    draft.setValue(type.name, name, text)
    if (bound?.quantity === name) setBound(null)
    setErrors((current) => Object.fromEntries(Object.entries(current).filter(([key]) => key !== name)))
  }

  const invalidCount = Object.keys(errors).length
  return (
    <form noValidate onSubmit={submit} className={`grid gap-4 ${computing ? 'computing' : ''}`}>
      {general.length > 0 && (
        <div role="alert" className="max-w-2xl border border-destructive bg-destructive-surface p-4">
          <p className="font-medium">{t('form.rejected')}</p>
          <ul className="list-disc pl-5 text-sm">
            {general.map((message, index) => (
              <li key={index}>{message}</li>
            ))}
          </ul>
        </div>
      )}
      {failure && <ErrorState error={failure} onRetry={() => void send()} />}
      {invalidCount > 0 && (
        <p className="flex items-center gap-1.5 font-medium text-destructive">
          <WarningCircle aria-hidden="true" weight="fill" size={18} className="shrink-0" />
          {t('form.summary')}: {invalidCount}
        </p>
      )}
      <div className="relative">
        {computing && <span aria-hidden="true" className="compute-scan" style={{ '--rows': type.inputs.length } as CSSProperties} />}
        <div
          aria-hidden="true"
          className={`${row} hidden border-b border-foreground pb-2 font-heading text-sm font-semibold text-muted-foreground sm:grid`}
        >
          <span />
          <span>{t('form.column.quantity')}</span>
          <span className="flex gap-2">
            <span className="w-36 text-right">{t('form.column.value')}</span>
            <span className="w-24 px-2.5">{t('form.unit')}</span>
          </span>
        </div>
        {type.inputs.map((input, index) => (
          <Field
            key={input.name}
            index={index}
            input={input}
            value={values[input.name] ?? ''}
            unit={units[input.name] ?? input.base_unit}
            error={errors[input.name]}
            bound={bound?.quantity === input.name ? bound : undefined}
            locked={submitting}
            onValue={(event) => change(input.name, event.target.value)}
            onUnit={(event) => draft.setUnit(type.name, input.name, event.target.value)}
          />
        ))}
      </div>
      <div className={row}>
        {computing && (
          <div className="col-span-full row-start-2 sm:col-span-1 sm:col-start-2 sm:row-start-1 sm:self-start">
            <ComputePlot />
          </div>
        )}
        <div className="col-start-2 grid gap-2 sm:col-start-3 sm:self-start">
          <Button type="submit" disabled={submitting} className="w-full">
            {t(submitting ? 'form.submitting' : 'form.submit')}
          </Button>
          <span aria-hidden="true" className="block h-0.5 bg-border">
            {submitting && <span className="send-rule" />}
          </span>
          <p role="status" className="min-h-5 text-sm text-muted-foreground">
            {stage && t(stageText[stage])}
          </p>
        </div>
      </div>
    </form>
  )
}
