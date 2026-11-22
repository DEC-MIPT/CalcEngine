import { ArrowRight } from '@phosphor-icons/react'
import { useCallback, useMemo } from 'react'
import { Link, useParams } from 'react-router'
import { api, unwrap, type ApiError } from '@/api/client'
import type { components } from '@/api/schema'
import { useRequest } from '@/api/useRequest'
import { Outputs } from '@/components/Outputs'
import { StoredChecks } from '@/components/StoredChecks'
import { DerivedRefusal, Refusal } from '@/components/Refusal'
import { ErrorState, LoadingState, NotFoundState } from '@/components/RequestStates'
import { Trace } from '@/components/Trace'
import { TraceRuler } from '@/components/TraceRuler'
import { isFoundationType } from '@/lib/foundationDesign'
import { FoundationEvidence } from '@/components/FoundationEvidence'
import { EditInputsLink } from '@/components/EditInputsLink'
import { buttonClass, secondaryButtonClass } from '@/components/ui/button'
import { VerdictStamp, type StampReveal } from '@/components/VerdictStamp'
import { Warnings } from '@/components/Warnings'
import { useDraft } from '@/form/draftContext'
import { useI18n } from '@/i18n/context'
import { outputRounding } from '@/lib/rounding'
import { outputLabels } from '@/lib/outputLabels'
import { symbolTable } from '@/lib/stepSymbol'
import { useTracePlayback, type PlaybackPhase } from '@/lib/useTracePlayback'
import { cn } from '@/lib/utils'

type Envelope = components['schemas']['ResultEnvelope']
type CheckReason = components['schemas']['CheckReason']
type DerivedReason = components['schemas']['DerivedViolation']
type CalculationType = components['schemas']['CalculationTypeView']

const loadTypes = () => unwrap(api.GET('/calculation-types'))

const isMissingResult = (error: ApiError) =>
  error.kind === 'api' &&
  (error.status === 404 ||
    (error.status === 422 &&
      error.fields.length > 0 &&
      error.fields.every((field) => field.location.join('.') === 'path.result_id')))

const SHOW_NORM_STATUS = false
const SHOW_ROUNDING_SOURCE = false

function stampReveal(phase: PlaybackPhase, envelope: Envelope): StampReveal {
  if (phase === 'playing') return 'pending'
  if (phase !== 'ended') return 'none'
  return envelope.verdict === 'pass' && envelope.warnings.length === 0 ? 'celebrate' : 'plain'
}

function CheckedResult({
  envelope,
  reason,
  editType,
  types,
}: {
  envelope: Envelope
  reason: CheckReason
  editType: string | null
  types: readonly CalculationType[] | undefined
}) {
  const { language } = useI18n()
  const playback = useTracePlayback(envelope.result_id, envelope.trace.length)
  const reveal = stampReveal(playback.phase, envelope)
  const symbols = useMemo(() => symbolTable(envelope.trace, types), [envelope.trace, types])
  const rounding = useMemo(() => outputRounding(envelope.outputs), [envelope.outputs])
  const labels = useMemo(() => outputLabels(types ?? [], language), [types, language])
  return (
    <>
      <TraceRuler steps={envelope.trace} verdict={envelope.verdict} playback={playback} reveal={reveal} symbols={symbols} />
      <VerdictStamp envelope={envelope} reason={reason} editType={editType} reveal={reveal} symbols={symbols} />
      <Outputs outputs={envelope.outputs} reveal={reveal} source={SHOW_ROUNDING_SOURCE} symbols={symbols} labels={labels} />
      <Warnings warnings={envelope.warnings} />
      <StoredChecks steps={envelope.trace} reason={reason} rounding={rounding} reveal={reveal} normStatus={SHOW_NORM_STATUS} labels={labels} symbols={symbols} />
      <Trace
        steps={envelope.trace}
        unverifiedStepCount={envelope.unverified_step_count}
        playback={playback}
        symbols={symbols}
        rounding={rounding}
        normStatus={SHOW_NORM_STATUS}
      />
    </>
  )
}

function DiagnosticResult({ envelope, reason, editType, types }: {
  envelope: Envelope
  reason: DerivedReason
  editType: string | null
  types: readonly CalculationType[] | undefined
}) {
  const { t } = useI18n()
  const symbols = useMemo(() => symbolTable(envelope.trace, types), [envelope.trace, types])
  return (
    <>
      <DerivedRefusal reason={reason} source={envelope.parameter_source} />
      <p className="mt-4 flex flex-wrap gap-3">
        {editType && <EditInputsLink type={editType} derivedCorrection={{ resultId: envelope.result_id, reason }} primary />}
        <Link to={`/calculations/${envelope.result_id}/report`} className={cn(buttonClass, editType && secondaryButtonClass)}>
          {t('result.toReport')}
          <ArrowRight aria-hidden="true" size={18} />
        </Link>
      </p>
      <Warnings warnings={envelope.warnings} />
      <Trace
        steps={envelope.trace}
        symbols={symbols}
        unverifiedStepCount={envelope.unverified_step_count}
        normStatus={SHOW_NORM_STATUS}
        title={t('refusal.diagnostic.title')}
        description={t('refusal.diagnostic.description')}
      />
    </>
  )
}

export function ResultScreen() {
  const { t } = useI18n()
  const { id } = useParams() as { id: string }
  const load = useCallback(
    () => unwrap(api.GET('/calculations/{result_id}', { params: { path: { result_id: id } } })),
    [id],
  )
  const { state, retry } = useRequest(load)
  const { state: typesState } = useRequest(loadTypes)
  const { sent } = useDraft()

  if (state.status === 'error' && isMissingResult(state.error)) {
    return <NotFoundState subject="result" />
  }
  const editType = state.status === 'ok' && sent?.resultId === state.data.result_id ? sent.type : null
  const checked = state.status === 'ok' && state.data.verdict_reason.kind === 'check'
  return (
    <>
      <h1 className="h1-ruled">{t('result.title')}</h1>
      {!checked && <TraceRuler />}
      {state.status === 'loading' && <LoadingState />}
      {state.status === 'error' && <ErrorState error={state.error} onRetry={retry} />}
      {state.status === 'ok' && (
        <>
          {state.data.verdict_reason.kind === 'bound' ? (
            <>
              <Refusal reason={state.data.verdict_reason} source={state.data.parameter_source} />
              <p className="mt-4 flex flex-wrap gap-3">
                {editType && <EditInputsLink type={editType} bound={state.data.verdict_reason.bound} primary />}
                <Link
                  to={`/calculations/${state.data.result_id}/report`}
                  className={cn(buttonClass, editType && secondaryButtonClass)}
                >
                  {t('result.toReport')}
                  <ArrowRight aria-hidden="true" size={18} />
                </Link>
              </p>
            </>
          ) : state.data.verdict_reason.kind === 'derived' ? (
            <DiagnosticResult
              key={state.data.result_id}
              envelope={state.data}
              reason={state.data.verdict_reason}
              editType={editType}
              types={typesState.status === 'ok' ? typesState.data : undefined}
            />
          ) : (
            <CheckedResult
              key={state.data.result_id}
              envelope={state.data}
              reason={state.data.verdict_reason}
              editType={editType}
              types={typesState.status === 'ok' ? typesState.data : undefined}
            />
          )}
          {(isFoundationType(editType) || state.data.trace.some((step) => step.step_id === 'Mx_base')) && (
            <FoundationEvidence resultId={state.data.result_id} inputHash={state.data.input_hash} />
          )}
        </>
      )}
    </>
  )
}
