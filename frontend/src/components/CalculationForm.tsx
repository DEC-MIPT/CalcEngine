import { WarningCircle } from '@phosphor-icons/react'
import { useState, type ChangeEvent, type FormEvent } from 'react'
import { useNavigate } from 'react-router'
import { api, unwrap, type ApiError } from '@/api/client'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import type { TextKey } from '@/i18n/dictionary'
import { pickText } from '@/i18n/translate'
import { unitLabel } from '@/i18n/units'
import { parseValue, type ParseError } from '@/form/parseValue'
import { mapFieldErrors } from '@/form/serverErrors'
import { ErrorState } from './RequestStates'
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

const fieldId = (name: string) => `field-${name}`

function FieldMessage({ id, children }: { id: string; children: string }) {
  return (
    <p id={id} className="flex items-start gap-2 text-sm text-destructive">
      <WarningCircle aria-hidden="true" weight="fill" size={18} className="mt-0.5 shrink-0" />
      {children}
    </p>
  )
}

interface FieldProps {
  input: Input
  value: string
  unit: string
  error: string | undefined
  onValue: (event: ChangeEvent<HTMLInputElement>) => void
  onUnit: (event: ChangeEvent<HTMLSelectElement>) => void
}

function Field({ input, value, unit, error, onValue, onUnit }: FieldProps) {
  const { t, language } = useI18n()
  const label = pickText(input.label, language)
  const hint = input.hint ? pickText(input.hint, language) : null
  const hintId = `hint-${input.name}`
  const errorId = `error-${input.name}`
  const describedBy = [hint ? hintId : null, error ? errorId : null].filter(Boolean).join(' ')
  const fixedUnit = input.whole_values_only || input.units.length === 1
  return (
    <div className="grid gap-1.5">
      <div className="flex items-baseline gap-2">
        <label htmlFor={fieldId(input.name)} className="font-medium">
          {label}
        </label>
        <span aria-hidden="true">
          <Formula latex={input.symbol} />
        </span>
      </div>
      {hint && (
        <p id={hintId} className="text-sm text-muted-foreground">
          {hint}
        </p>
      )}
      <div className="flex gap-2">
        <input
          id={fieldId(input.name)}
          name={input.name}
          type="text"
          inputMode="decimal"
          autoComplete="off"
          value={value}
          onChange={onValue}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy || undefined}
          className="min-h-9 w-full min-w-0 border border-input bg-card px-3 py-1.5 aria-invalid:border-destructive aria-invalid:border-2"
        />
        {fixedUnit ? (
          <span className="flex min-h-9 min-w-16 items-center">{unitLabel(input.base_unit, language)}</span>
        ) : (
          <select
            value={unit}
            onChange={onUnit}
            aria-label={`${t('form.unit')}: ${label}`}
            className="min-h-9 min-w-28 border border-input bg-card px-2"
          >
            {input.units.map((code) => (
              <option key={code} value={code}>
                {unitLabel(code, language)}
              </option>
            ))}
          </select>
        )}
      </div>
      {error && <FieldMessage id={errorId}>{error}</FieldMessage>}
    </div>
  )
}

export function CalculationForm({ type }: { type: CalculationType }) {
  const { t } = useI18n()
  const navigate = useNavigate()
  const [values, setValues] = useState<Record<string, string>>({})
  const [units, setUnits] = useState<Record<string, string>>({})
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [general, setGeneral] = useState<string[]>([])
  const [failure, setFailure] = useState<ApiError | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function send() {
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

    setSubmitting(true)
    const result = await unwrap(
      api.POST('/calculations', { body: { calculation_type: type.name, inputs } }),
    )
    setSubmitting(false)
    if (result.ok) {
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

  function change(name: string, text: string) {
    setValues((current) => ({ ...current, [name]: text }))
    setErrors((current) => Object.fromEntries(Object.entries(current).filter(([key]) => key !== name)))
  }

  return (
    <form noValidate onSubmit={submit} className="grid max-w-2xl gap-6">
      {general.length > 0 && (
        <div role="alert" className="border border-destructive border-l-4 bg-destructive-surface p-4">
          <p className="font-medium">{t('form.rejected')}</p>
          <ul className="list-disc pl-5 text-sm">
            {general.map((message, index) => (
              <li key={index}>{message}</li>
            ))}
          </ul>
        </div>
      )}
      {failure && <ErrorState error={failure} onRetry={() => void send()} />}
      {type.inputs.map((input) => (
        <Field
          key={input.name}
          input={input}
          value={values[input.name] ?? ''}
          unit={units[input.name] ?? input.base_unit}
          error={errors[input.name]}
          onValue={(event) => change(input.name, event.target.value)}
          onUnit={(event) => setUnits((current) => ({ ...current, [input.name]: event.target.value }))}
        />
      ))}
      <div>
        <Button type="submit" disabled={submitting}>
          {t(submitting ? 'form.submitting' : 'form.submit')}
        </Button>
      </div>
    </form>
  )
}
