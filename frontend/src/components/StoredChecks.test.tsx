import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsCentralEnvelope, loadsFailEnvelope } from '@/mocks/fixtures'
import { outputRounding } from '@/lib/rounding'
import { expectNoA11yViolations } from '@/test/axe'
import { StoredChecks } from './StoredChecks'

type Check = Extract<components['schemas']['ResultEnvelope']['trace'][number], { kind: 'check' }>
const checks = loadsCentralEnvelope.trace.filter((step) => step.kind === 'check')

function reason(envelope: components['schemas']['ResultEnvelope']) {
  if (envelope.verdict_reason.kind !== 'check') throw new Error('Expected a completed result.')
  return envelope.verdict_reason
}

describe('stored check presentation', () => {
  it('renders sparse stored checks from their operands without guessing missing labels', () => {
    const sparse: Check = { ...checks[0], substitutions: [], norm_refs: [] }
    const { container } = render(
      <I18nProvider initialLanguage="en"><StoredChecks steps={[sparse]} reason={{ kind: 'check', step_id: 'another_stored_reason' }} labels={new Map([['p', 'Mean pressure']])} /></I18nProvider>,
    )
    expect(screen.getByRole('heading', { name: 'Check 1' })).toBeInTheDocument()
    expect(screen.getByRole('img', { name: sparse.expression })).toBeInTheDocument()
    expect(container.querySelector('[data-comparison]')).toHaveTextContent('120 kPa ≤less than or equal to 152.02 kPa')
    expect(container.querySelector('[data-deciding="true"]')).toBeNull()
    expect(screen.getByText('another_stored_reason')).toBeInTheDocument()
  })

  it('preserves supplied check order and marks the stored deciding identity', async () => {
    const { container } = render(
      <I18nProvider><StoredChecks steps={loadsCentralEnvelope.trace} reason={reason(loadsCentralEnvelope)} normStatus={false} /></I18nProvider>,
    )
    const rows = [...container.querySelectorAll('[data-check-step]')]
    expect(rows.map((row) => row.getAttribute('data-check-step'))).toEqual(checks.map((step) => step.step_id))
    expect(container.querySelector('[data-deciding="true"]')).toHaveAttribute('data-check-step', loadsCentralEnvelope.verdict_reason.step_id)
    expect(screen.getAllByText('Проверка выполнена')).toHaveLength(4)
    expect(screen.getByRole('heading', { name: 'Проверка 4' })).toBeInTheDocument()
    expect(screen.queryByText('не проверено')).not.toBeInTheDocument()
    await expectNoA11yViolations(container)
  })

  it('reports stored failed checks and sources without calculating a verdict', async () => {
    const { container } = render(
      <I18nProvider initialLanguage="en"><StoredChecks steps={loadsFailEnvelope.trace} reason={reason(loadsFailEnvelope)} /></I18nProvider>,
    )
    expect(screen.getByText('Determines the verdict')).toBeInTheDocument()
    expect(screen.getAllByText('unverified')).toHaveLength(4)
    const deciding = container.querySelector<HTMLElement>('[data-deciding="true"]')!
    expect(deciding).toHaveAttribute('data-check-step', loadsFailEnvelope.verdict_reason.step_id)
    expect(within(deciding).getByText('Check failed')).toBeInTheDocument()
    await expectNoA11yViolations(container)
  })

  it('keeps the pending body inaccessible until the existing reveal completes', () => {
    const { container, rerender } = render(
      <I18nProvider><StoredChecks steps={checks} reason={reason(loadsCentralEnvelope)} reveal="pending" /></I18nProvider>,
    )
    expect(container.querySelector('[inert]')).toHaveClass('invisible')
    expect(container.querySelector('[data-checks-status]')).toHaveTextContent('ВЫПОЛНЕНИЕ РАСЧЁТА')
    rerender(<I18nProvider><StoredChecks steps={checks} reason={reason(loadsCentralEnvelope)} reveal="plain" /></I18nProvider>)
    expect(container.querySelector('[inert]')).toBeNull()
    expect(container.querySelector('[data-checks-status]')).toBeNull()
  })

  it('leaves close failed operands distinguishable and permits keyboard formula scrolling', async () => {
    const user = userEvent.setup()
    const step: Check = {
      ...checks[0],
      result: { value: 152.02000000000004, unit: 'kPa' },
      right: { value: 152.02, unit: 'kPa' },
      substitutions: [
        { symbol: 'p', value: 152.02000000000004, unit: 'kPa' },
        { symbol: 'R', value: 152.02, unit: 'kPa' },
      ],
      passed: false,
      norm_refs: [],
    }
    const { container } = render(
      <I18nProvider initialLanguage="en"><StoredChecks steps={[step]} reason={{ kind: 'check', step_id: step.step_id }} rounding={outputRounding(loadsCentralEnvelope.outputs)} labels={new Map([['p', 'Mean pressure']])} /></I18nProvider>,
    )
    expect(screen.getByRole('heading', { name: 'Mean pressure' })).toBeInTheDocument()
    expect(container.querySelector('[data-comparison]')).toHaveTextContent('152.02000000000004 kPa ≤less than or equal to 152.02 kPa')
    await user.tab()
    expect(screen.getByRole('region', { name: `Check formula: ${step.step_id}` })).toHaveFocus()
  })
})
