import { render, screen, within } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import type { ReactNode } from 'react'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsBiaxialEnvelope, loadsCentralEnvelope, loadsFailEnvelope } from '@/mocks/fixtures'
import { outputRounding } from '@/lib/rounding'
import { Outputs } from './Outputs'
import { StoredChecks } from './StoredChecks'
import { VerdictStamp } from './VerdictStamp'
import { Trace } from './Trace'

type Envelope = components['schemas']['ResultEnvelope']
type Check = Extract<Envelope['trace'][number], { kind: 'check' }>
type Rule = components['schemas']['RoundingRule']

function show(children: ReactNode) {
  return render(<RouterProvider router={createMemoryRouter([{
    path: '/', element: <I18nProvider initialLanguage="en">{children}</I18nProvider>,
  }])} />)
}

function checks(envelope: Envelope): Check[] {
  return envelope.trace.filter((step): step is Check => step.kind === 'check')
}

function checked(envelope: Envelope) {
  if (envelope.verdict_reason.kind !== 'check') throw new Error('A completed fixture is required')
  return <StoredChecks steps={envelope.trace} reason={envelope.verdict_reason} rounding={outputRounding(envelope.outputs)} />
}

const outputOrder = ['R', 'p', 'p_x_min', 'p_x_max', 'p_y_min', 'p_y_max', 'p_corner_pp', 'p_corner_pm', 'p_corner_mp', 'p_corner_mm']
const checkOrder = ['p_le_R', 'p_x_max_le_limit', 'p_y_max_le_limit', 'p_corner_max_le_limit']

function syntheticCheck(operator: Check['operator'], passed: boolean, left: number, right: number): Check {
  return {
    ...checks(loadsCentralEnvelope)[0], norm_refs: [], step_id: 'presentation_only', operator, passed,
    expression: 'L \\mathrel{?} U', result: { value: left, unit: 'kPa' }, right: { value: right, unit: 'kPa' },
    substitutions: [{ symbol: 'p', value: left, unit: 'kPa' }, { symbol: 'R', value: right, unit: 'kPa' }],
  }
}

describe('loads result presentation contract', () => {
  it.each([loadsCentralEnvelope, loadsBiaxialEnvelope, loadsFailEnvelope])('renders the ten supplied outputs in stored order without mutation', (envelope) => {
    const before = structuredClone(envelope)
    show(<Outputs outputs={envelope.outputs} source={false} />)
    const rows = [...document.querySelectorAll('[data-output]')]
    expect(rows.map((row) => row.getAttribute('data-output'))).toEqual(outputOrder)
    rows.forEach((row, index) => {
      expect(row.querySelector('[data-value]')).toHaveTextContent(envelope.outputs[index].value.toFixed(2))
      expect(row).toHaveTextContent('kPa')
      expect(row.querySelector('[data-rounding]')).toHaveTextContent('to nearest, ties up; decimal places: 2')
    })
    expect(envelope).toEqual(before)
  })

  it.each([
    ['half_up', 2, 1.245, '1.25'], ['half_even', 2, 1.245, '1.24'],
    ['half_up', 2, -1.245, '-1.25'], ['half_even', 2, -1.245, '-1.24'],
    ['half_even', 0, 2.5, '2'], ['half_up', 0, 2.5, '3'],
    ['half_even', 3, 2, '2.000'],
  ] as const)('honors supplied %s/%s display precision for %s', (mode, decimals, value, expected) => {
    show(<Outputs outputs={[{ ...loadsCentralEnvelope.outputs[0], value, rounding_rule: { mode, decimals } }]} source={false} />)
    expect(document.querySelector('[data-value]')).toHaveTextContent(expected)
    expect(document.querySelector('[data-rounding]')).toHaveTextContent(`decimal places: ${decimals}`)
  })

  it.each([loadsCentralEnvelope, loadsBiaxialEnvelope, loadsFailEnvelope])('keeps all four stored checks and highlights only the supplied deciding step', (envelope) => {
    show(checked(envelope))
    const formulas = [...document.querySelectorAll('[data-check-step] [role="region"]')]
    expect(formulas.map((region) => region.querySelector('[role="img"][aria-label]')?.getAttribute('aria-label') ?? region.querySelector('[data-fallback]')?.textContent)).toEqual(checks(envelope).map((step) => step.expression))
    formulas.forEach((region, index) => {
      const formula = region.querySelector('[role="img"][aria-label]')
      if (formula) expect(within(region as HTMLElement).getByRole('img', { name: checks(envelope)[index].expression })).toBeInTheDocument()
      else expect(region.querySelector('[data-fallback]')?.closest('[aria-hidden="true"]')).toBeNull()
    })
    expect(checks(envelope).map((step) => step.step_id)).toEqual(checkOrder)
    expect([...document.querySelectorAll('[data-check-step]')].map((row) => row.getAttribute('data-check-step'))).toEqual(checkOrder)
    expect(document.querySelector('[data-deciding="true"]')).toHaveAttribute('data-check-step', envelope.verdict_reason.kind === 'check' ? envelope.verdict_reason.step_id : '')
    for (const step of checks(envelope)) {
      const card = document.querySelector(`[data-check-step="${step.step_id}"]`)!
      expect(card).toHaveTextContent(step.passed ? 'Check passed' : 'Check failed')
      expect(card.querySelector('[data-comparison]')).toHaveTextContent('≤less than or equal to')
    }
  })

  it('prints supplied substitutions and the stored right operand without deriving a limit from other values', () => {
    const step: Check = { ...syntheticCheck('le', true, 7.1234567, 37.7654321),
      substitutions: [{ symbol: 'sentinel_left', value: 91.2345678, unit: 'kPa' }, { symbol: 'sentinel_right', value: 92.3456789, unit: 'kPa' }],
    }
    show(<><StoredChecks steps={[step]} reason={{ kind: 'check', step_id: step.step_id }} /><Trace steps={[step]} unverifiedStepCount={0} /></>)
    expect(document.querySelector('[data-check-step] [data-comparison]')).toHaveTextContent('7.1234567 kPa ≤less than or equal to 37.7654321 kPa')
    const trace = screen.getByRole('region', { name: 'Calculation trace' })
    expect(trace).toHaveTextContent('91.2345678 kPa')
    expect(trace).toHaveTextContent('92.3456789 kPa')
  })

  it('uses the stored reason instead of deriving a replacement from failing checks', () => {
    const steps = checks(loadsFailEnvelope)
    show(<VerdictStamp envelope={loadsFailEnvelope} reason={{ kind: 'check', step_id: steps[3].step_id }} />)
    expect(document.querySelector('[data-check]')).toHaveAttribute('data-check', steps[3].step_id)
    expect(screen.getByRole('region', { name: 'Check failed' })).toBeInTheDocument()
  })

  it.each([
    ['le', false, 1.004, 1.003, '≤', 'less than or equal to'],
    ['lt', true, 1.003, 1.004, '<', 'less than'],
    ['ge', false, 1.003, 1.004, '≥', 'greater than or equal to'],
    ['gt', true, 1.004, 1.003, '>', 'greater than'],
  ] as const)('does not replace a %s boundary comparison with misleading equal rounded operands', (operator, passed, left, right, symbol, spoken) => {
    const step = syntheticCheck(operator, passed, left, right)
    const rule: Rule = { mode: 'half_up', decimals: 2 }
    show(<StoredChecks steps={[step]} reason={{ kind: 'check', step_id: step.step_id }} rounding={new Map([['p', rule], ['R', rule]])} />)
    expect(screen.getByText(spoken, { exact: true })).toBeInTheDocument()
    expect(screen.getByText(symbol, { exact: true })).toBeInTheDocument()
    expect(screen.getAllByText(new RegExp(`${left} kPa`, 'u')).length).toBeGreaterThan(0)
    expect(screen.getAllByText(new RegExp(`${right} kPa`, 'u')).length).toBeGreaterThan(0)
    expect(screen.getByText(passed ? 'Check passed' : 'Check failed', { exact: true })).toBeInTheDocument()
  })

  it('keeps a tiny positive failed operand distinct from zero instead of printing a false equality', () => {
    const step = syntheticCheck('le', false, 1e-25, 0)
    const envelope: Envelope = { ...loadsCentralEnvelope, verdict: 'fail', trace: [step], verdict_reason: { kind: 'check', step_id: step.step_id } }
    show(<>{checked(envelope)}<VerdictStamp envelope={envelope} reason={{ kind: 'check', step_id: step.step_id }} /></>)
    expect(screen.getAllByText(/1[eE]−?-?25 kPa/u).length).toBeGreaterThan(0)
    const stamp = screen.getByRole('region', { name: 'Check failed' })
    expect(stamp.querySelector('[data-check] p')).toHaveTextContent(/1[eE]−?-?25 kPa/u)
    expect(stamp.querySelector('[data-check] p')).not.toHaveTextContent(/^0 kPa/u)
  })

  it('preserves the supplied pass flag even for a deliberately inconsistent presentation-only envelope', () => {
    const step = syntheticCheck('le', true, 90, 10)
    show(<StoredChecks steps={[step]} reason={{ kind: 'check', step_id: step.step_id }} />)
    expect(screen.getByText('Check passed', { exact: true })).toBeInTheDocument()
    expect(screen.queryByText('Check failed', { exact: true })).not.toBeInTheDocument()
    expect(document.querySelector('[data-check-step] [role="img"][aria-label]')).toHaveAttribute('aria-label', step.expression)
  })
})
