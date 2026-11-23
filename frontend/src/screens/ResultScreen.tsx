import { ArrowRight } from '@phosphor-icons/react'
import { useCallback, useEffect, useMemo } from 'react'
import { Link, useLocation, useNavigate, useParams } from 'react-router'
import { api, unwrap, type ApiError } from '@/api/client'
import type { components } from '@/api/schema'
import { useRequest } from '@/api/useRequest'
import { Outputs } from '@/components/Outputs'
import { StoredChecks } from '@/components/StoredChecks'
import { DerivedRefusal, Refusal } from '@/components/Refusal'
import { ErrorState, LoadingState, NotFoundState } from '@/components/RequestStates'
import { Trace } from '@/components/Trace'
import { TraceRuler } from '@/components/TraceRuler'
import { DemoResultDisplay } from '@/lib/resultDisplay'
import { isFoundationType, WEIGHTS_TYPE } from '@/lib/foundationDesign'
import { FoundationEvidence } from '@/components/FoundationEvidence'
import { EditInputsLink } from '@/components/EditInputsLink'
import { buttonClass, secondaryButtonClass } from '@/components/ui/button'
import { VerdictStamp, type StampReveal } from '@/components/VerdictStamp'
import { Warnings } from '@/components/Warnings'
import { useDraft, type SentForm } from '@/form/draftContext'
import { useI18n } from '@/i18n/context'
import { outputRounding } from '@/lib/rounding'
import { outputLabels } from '@/lib/outputLabels'
import { symbolTable } from '@/lib/stepSymbol'
import { useTracePlayback, type PlaybackPhase } from '@/lib/useTracePlayback'
import { focusAnchor, traceStepAnchor } from '@/lib/jumpTo'
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
  editExample,
  types,
  hideEngineerSource,
}: {
  envelope: Envelope
  reason: CheckReason
  editType: string | null
  editExample?: SentForm['example']
  types: readonly CalculationType[] | undefined
  hideEngineerSource: boolean
}) {
  const { t, language } = useI18n()
  const { hash } = useLocation()
  const playback = useTracePlayback(envelope.result_id, envelope.trace.length, !hideEngineerSource || !traceStepAnchor(hash, envelope.trace.length))
  const onStepLink = useDemoStepLink(hideEngineerSource)
  const reveal = stampReveal(playback.phase, envelope)
  const symbols = useMemo(() => symbolTable(envelope.trace, types), [envelope.trace, types])
  const rounding = useMemo(() => outputRounding(envelope.outputs), [envelope.outputs])
  const labels = useMemo(() => outputLabels(types ?? [], language), [types, language])
  return (
    <>
      <TraceRuler steps={envelope.trace} verdict={envelope.verdict} playback={playback} reveal={reveal} symbols={symbols} scrollLabel={hideEngineerSource ? t('trace.ruler') : undefined} onStepLink={onStepLink} />
      <VerdictStamp envelope={envelope} reason={reason} editType={editType} editExample={editExample} reveal={reveal} symbols={symbols} />
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
        hideEngineerSource={hideEngineerSource}
        fallbackNormRefs={envelope.norm_refs}
      />
    </>
  )
}

function useDemoStepLink(demo: boolean) {
  const navigate = useNavigate()
  return demo ? (id: string) => void navigate({ hash: `#${id}` }, { replace: true, preventScrollReset: true }) : undefined
}

function DiagnosticResult({ envelope, reason, editType, editExample, types, hideEngineerSource }: {
  envelope: Envelope
  reason: DerivedReason
  editType: string | null
  editExample?: SentForm['example']
  types: readonly CalculationType[] | undefined
  hideEngineerSource: boolean
}) {
  const { t } = useI18n()
  const onStepLink = useDemoStepLink(hideEngineerSource)
  const symbols = useMemo(() => symbolTable(envelope.trace, types), [envelope.trace, types])
  return (
    <>
      {hideEngineerSource && (
        <TraceRuler steps={envelope.trace} verdict={envelope.verdict} symbols={symbols} scrollLabel={t('trace.ruler')} onStepLink={onStepLink} />
      )}
      <DerivedRefusal
        reason={reason}
        source={envelope.parameter_source}
        hideEngineerSource={hideEngineerSource}
        fallbackNormRefs={envelope.norm_refs}
      />
      <p className="mt-4 flex flex-wrap gap-3">
        {editType && <EditInputsLink type={editType} example={editExample} derivedCorrection={{ resultId: envelope.result_id, reason }} primary />}
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
        hideEngineerSource={hideEngineerSource}
        fallbackNormRefs={envelope.norm_refs}
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
  const outputs = state.status === 'ok' ? state.data.outputs : undefined
  const rounding = useMemo(() => outputs && outputRounding(outputs), [outputs])

  const { hash } = useLocation()
  const envelope = state.status === 'ok' ? state.data : undefined
  const hideEngineerSource = envelope?.trace.some((step) => step.step_id === 'G_sum') ?? false
  const anchor = hideEngineerSource ? traceStepAnchor(hash, envelope?.trace.length ?? 0) : undefined
  const resultId = envelope?.result_id
  useEffect(() => {
    if (!anchor) return
    const frame = requestAnimationFrame(() => focusAnchor(anchor))
    return () => cancelAnimationFrame(frame)
  }, [anchor, resultId])

  if (state.status === 'error' && isMissingResult(state.error)) {
    return <NotFoundState subject="result" />
  }
  const submitted = state.status === 'ok' && sent?.resultId === state.data.result_id ? sent : null
  const editType = submitted?.type ?? null
  const editExample = submitted?.example
  const checked = state.status === 'ok' && state.data.verdict_reason.kind === 'check'
  const showRuler = checked || (hideEngineerSource && state.status === 'ok' && state.data.verdict_reason.kind === 'derived')
  return (
    <>
      <h1 className="h1-ruled">{t('result.title')}</h1>
      {!showRuler && <TraceRuler />}
      {state.status === 'loading' && <LoadingState />}
      {state.status === 'error' && <ErrorState error={state.error} onRetry={retry} />}
      {state.status === 'ok' && (
        <DemoResultDisplay.Provider value={hideEngineerSource || editType === WEIGHTS_TYPE}>
          {state.data.verdict_reason.kind === 'bound' ? (
            <>
              <Refusal reason={state.data.verdict_reason} source={state.data.parameter_source} />
              <p className="mt-4 flex flex-wrap gap-3">
                {editType && <EditInputsLink type={editType} example={editExample} bound={state.data.verdict_reason.bound} primary />}
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
              editExample={editExample}
              types={typesState.status === 'ok' ? typesState.data : undefined}
              hideEngineerSource={hideEngineerSource}
            />
          ) : (
            <CheckedResult
              key={state.data.result_id}
              envelope={state.data}
              reason={state.data.verdict_reason}
              editType={editType}
              editExample={editExample}
              types={typesState.status === 'ok' ? typesState.data : undefined}
              hideEngineerSource={hideEngineerSource}
            />
          )}
          {(isFoundationType(editType) || state.data.trace.some((step) => step.step_id === 'Mx_base')) && (
            <FoundationEvidence resultId={state.data.result_id} inputHash={state.data.input_hash} rounding={hideEngineerSource ? rounding : undefined} />
          )}
        </DemoResultDisplay.Provider>
      )}
    </>
  )
}
