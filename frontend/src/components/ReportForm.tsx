import { CheckCircle, DownloadSimple, WarningCircle } from '@phosphor-icons/react'
import { useState, type FormEvent } from 'react'
import { api, errorOf, type ApiError } from '@/api/client'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import type { TextKey } from '@/i18n/dictionary'
import { fileNameFrom, saveFile } from '@/report/download'
import { mapReportErrors } from '@/report/errors'
import { ErrorState } from './RequestStates'
import { Button } from './ui/button'

type ReportRequest = components['schemas']['ReportRequest']
type TitleName = keyof ReportRequest['title']
type Role = 'developer' | 'normative_control' | 'checker'
type Person = { surname: string; date: string }

const TITLE_FIELDS: readonly { name: TitleName; column: string; required: boolean }[] = [
  { name: 'designation', column: '1', required: true },
  { name: 'document_name', column: '5', required: true },
  { name: 'documentation_kind', column: '6', required: false },
  { name: 'organization', column: '9', required: true },
]

const ROLES: readonly { role: Role; required: boolean }[] = [
  { role: 'developer', required: true },
  { role: 'normative_control', required: true },
  { role: 'checker', required: false },
]

const FIELD_KEYS = [
  ...TITLE_FIELDS.map(({ name }) => `title.${name}`),
  ...ROLES.flatMap(({ role }) => [`${role}.surname`, `${role}.date`]),
  'signature_block',
]

const fieldId = (key: string) => `report-${key.replace('.', '-')}`
const errorId = (key: string) => `${fieldId(key)}-error`

const input =
  'min-h-9 w-full min-w-0 border border-input bg-card px-2.5 py-1.5 focus-visible:outline-offset-[-1px] aria-invalid:border-destructive aria-invalid:focus-visible:outline-destructive'
const titleRow =
  'grid grid-cols-[3.5rem_minmax(0,1fr)] gap-x-3 gap-y-1.5 border-b border-border py-2.5 sm:grid-cols-[3.5rem_minmax(0,1fr)_minmax(0,24rem)] sm:items-center'
const personRow =
  'grid grid-cols-2 gap-x-3 gap-y-1.5 border-b border-border py-2.5 sm:grid-cols-[minmax(0,1fr)_minmax(0,16rem)_10rem] sm:items-start'

function FieldMessage({ id, children }: { id: string; children: string }) {
  return (
    <p id={id} className="flex items-start gap-1.5 text-sm text-destructive">
      <WarningCircle aria-hidden="true" weight="fill" size={16} className="mt-0.5 shrink-0" />
      {children}
    </p>
  )
}

function TextField({
  fieldKey,
  label,
  type = 'text',
  value,
  error,
  onChange,
}: {
  fieldKey: string
  label?: string
  type?: 'text' | 'date'
  value: string
  error: string | undefined
  onChange: (value: string) => void
}) {
  return (
    <div className="grid gap-1">
      <input
        id={fieldId(fieldKey)}
        type={type}
        aria-label={label}
        value={value}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? errorId(fieldKey) : undefined}
        onChange={(event) => onChange(event.target.value)}
        className={`${input} ${type === 'date' ? 'font-mono' : ''}`}
      />
      {error && <FieldMessage id={errorId(fieldKey)}>{error}</FieldMessage>}
    </div>
  )
}

function validate(
  title: Record<TitleName, string>,
  signatureBlock: boolean,
  people: Record<Role, Person>,
): Record<string, TextKey> {
  const invalid: Record<string, TextKey> = {}
  for (const { name, required } of TITLE_FIELDS) {
    if (required && !title[name].trim()) invalid[`title.${name}`] = 'report.error.required'
  }
  if (!signatureBlock) return invalid
  for (const { role, required } of ROLES) {
    const { surname, date } = people[role]
    const given = surname.trim() !== '' || date !== ''
    if (!required && !given) continue
    const message = required ? 'report.error.required' : 'report.error.checkerPair'
    if (!surname.trim()) invalid[`${role}.surname`] = message
    if (!date) invalid[`${role}.date`] = message
  }
  return invalid
}

function requestBody(
  title: Record<TitleName, string>,
  signatureBlock: boolean,
  people: Record<Role, Person>,
): ReportRequest {
  const body: ReportRequest = { title, signature_block: signatureBlock }
  if (!signatureBlock) return body
  for (const { role, required } of ROLES) {
    const { surname, date } = people[role]
    if (required || surname.trim() !== '') body[role] = { surname, date }
  }
  return body
}

const emptyPerson: Person = { surname: '', date: '' }

export function ReportForm({ resultId }: { resultId: string }) {
  const { t } = useI18n()
  const [title, setTitle] = useState<Record<TitleName, string>>({
    designation: '',
    document_name: '',
    documentation_kind: '',
    organization: '',
  })
  const [signatureBlock, setSignatureBlock] = useState(true)
  const [people, setPeople] = useState<Record<Role, Person>>({
    developer: emptyPerson,
    normative_control: emptyPerson,
    checker: emptyPerson,
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [general, setGeneral] = useState<string[]>([])
  const [failure, setFailure] = useState<ApiError | null>(null)
  const [saved, setSaved] = useState<string | null>(null)
  const [sending, setSending] = useState(false)

  function clear(key: string) {
    setErrors((current) => Object.fromEntries(Object.entries(current).filter(([name]) => name !== key)))
    setSaved(null)
  }

  async function send() {
    const invalid = validate(title, signatureBlock, people)
    setErrors(Object.fromEntries(Object.entries(invalid).map(([key, message]) => [key, t(message)])))
    setGeneral([])
    setFailure(null)
    setSaved(null)
    const first = FIELD_KEYS.find((key) => key in invalid)
    if (first) {
      document.getElementById(fieldId(first))?.focus()
      return
    }
    setSending(true)
    let outcome
    try {
      outcome = await api.POST('/calculations/{result_id}/report', {
        params: { path: { result_id: resultId } },
        body: requestBody(title, signatureBlock, people),
        parseAs: 'blob',
      })
    } catch {
      setSending(false)
      setFailure({ kind: 'network' })
      return
    }
    setSending(false)
    if (outcome.error === undefined) {
      const name = fileNameFrom(outcome.response.headers.get('Content-Disposition'), `dec-report-${resultId}.docx`)
      saveFile(outcome.data as Blob, name)
      setSaved(name)
      return
    }
    const error = errorOf(outcome.error, outcome.response.status)
    if (error.kind === 'api' && error.status === 422) {
      const mapped = mapReportErrors(error.fields, FIELD_KEYS)
      setErrors(mapped.byField)
      setGeneral(mapped.general.length === 0 && Object.keys(mapped.byField).length === 0 ? [error.message] : mapped.general)
    } else {
      setFailure(error)
    }
  }

  function submit(event: FormEvent) {
    event.preventDefault()
    void send()
  }

  const invalidCount = Object.keys(errors).length
  return (
    <form noValidate onSubmit={submit} className="grid gap-6">
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

      <fieldset>
        <legend className="mb-1 font-heading text-xl font-semibold">{t('report.titleBlock')}</legend>
        <p className="mb-2 text-sm text-muted-foreground">{t('report.titleBlockHint')}</p>
        {TITLE_FIELDS.map(({ name, column, required }) => {
          const key = `title.${name}`
          return (
            <div key={name} className={titleRow}>
              <span aria-hidden="true" className="row-span-2 pt-0.5 font-mono text-sm text-muted-foreground sm:row-span-1 sm:pt-0">
                {t('report.column')} {column}
              </span>
              <label htmlFor={fieldId(key)} className="font-medium">
                {t(`report.field.${name}`)}
                {!required && <span className="font-normal text-muted-foreground"> · {t('report.optional')}</span>}
              </label>
              <div className="col-start-2 sm:col-start-3">
                <TextField
                  fieldKey={key}
                  value={title[name]}
                  error={errors[key]}
                  onChange={(value) => {
                    setTitle((current) => ({ ...current, [name]: value }))
                    clear(key)
                  }}
                />
              </div>
            </div>
          )
        })}
      </fieldset>

      <fieldset className="grid gap-3">
        <legend className="mb-1 font-heading text-xl font-semibold">{t('report.signatures')}</legend>
        <div className="flex w-fit items-start gap-2.5">
          <input
            id={fieldId('signature_block')}
            type="checkbox"
            role="switch"
            checked={signatureBlock}
            aria-describedby="report-signature-hint"
            onChange={(event) => {
              setSignatureBlock(event.target.checked)
              setErrors({})
              setSaved(null)
            }}
            className="mt-1 size-4 shrink-0 cursor-pointer accent-primary"
          />
          <div className="grid gap-0.5">
            <label htmlFor={fieldId('signature_block')} className="cursor-pointer font-medium">
              {t('report.signatureBlock')}
            </label>
            <p id="report-signature-hint" className="text-sm text-muted-foreground">
              {t(signatureBlock ? 'report.signatureBlockOn' : 'report.signatureBlockOff')}
            </p>
          </div>
        </div>
        {errors.signature_block && <FieldMessage id={errorId('signature_block')}>{errors.signature_block}</FieldMessage>}
        {signatureBlock && (
          <div data-signatories>
            <div
              aria-hidden="true"
              className="hidden grid-cols-[minmax(0,1fr)_minmax(0,16rem)_10rem] gap-x-3 border-b border-foreground pb-2 font-heading text-sm font-semibold text-muted-foreground sm:grid"
            >
              <span>{t('report.role')}</span>
              <span>{t('report.surname')}</span>
              <span>{t('report.date')}</span>
            </div>
            {ROLES.map(({ role, required }) => (
              <div key={role} className={personRow} data-role={role}>
                <p className="col-span-full font-medium sm:col-span-1 sm:pt-1.5">
                  {t(`report.role.${role}`)}
                  {!required && <span className="font-normal text-muted-foreground"> · {t('report.optional')}</span>}
                </p>
                {(['surname', 'date'] as const).map((part) => {
                  const key = `${role}.${part}`
                  return (
                    <TextField
                      key={part}
                      fieldKey={key}
                      type={part === 'date' ? 'date' : 'text'}
                      label={`${t(`report.role.${role}`)}: ${t(`report.${part}`)}`}
                      value={people[role][part]}
                      error={errors[key]}
                      onChange={(value) => {
                        setPeople((current) => ({ ...current, [role]: { ...current[role], [part]: value } }))
                        clear(key)
                      }}
                    />
                  )
                })}
              </div>
            ))}
          </div>
        )}
      </fieldset>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <Button type="submit" disabled={sending}>
          <DownloadSimple aria-hidden="true" size={18} />
          {t(sending ? 'report.submitting' : 'report.submit')}
        </Button>
        {saved && (
          <p role="status" className="inline-flex items-center gap-1.5 text-sm">
            <CheckCircle aria-hidden="true" weight="fill" size={18} className="text-primary" />
            {t('report.saved')}: <span className="font-mono">{saved}</span>
          </p>
        )}
      </div>
    </form>
  )
}
