import { fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsCentralEnvelope, loadsContactRefusalEnvelope, passEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { Trace } from './Trace'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
const steps: readonly Step[] = loadsCentralEnvelope.trace

function show(trace: readonly Step[] = steps) {
  return render(<I18nProvider initialLanguage="en"><Trace steps={trace} unverifiedStepCount={0} /></I18nProvider>)
}

const rows = () => [...document.querySelectorAll<HTMLElement>('[data-step]')]
const header = (row: HTMLElement) => within(row).getByRole('button')
const details = (row: HTMLElement) => document.getElementById(header(row).getAttribute('aria-controls')!)!

describe('compact stored loads trace', () => {
  it('places the captured pressure and source steps under the correct semantic section boundaries', () => {
    show()
    expect(rows().flatMap((row) => {
      const heading = row.querySelector('[data-trace-section]')
      return heading ? [[row.dataset.step, heading.textContent]] : []
    })).toEqual([
      ['gamma_c1', 'Design resistance R'],
      ['A', 'Geometry and load transfer'],
      ['gamma_mt', 'Mean pressure'],
      ['p_x_min', 'Pressures along X'],
      ['p_y_min', 'Pressures along Y'],
      ['corner_component_pp', 'Corner pressures'],
      ['p_corner_min', 'Minimum, maximum and contact condition'],
      ['edge_limit_multiplier', 'Pressure limits and checks'],
    ])
  })

  it.each([loadsCentralEnvelope.trace, loadsContactRefusalEnvelope.trace].map((trace) => ({ trace })))('starts with complete summaries and collapsed details in the original flat list', ({ trace }) => {
    const before = structuredClone(trace)
    show(trace)
    expect(rows().map((row) => row.dataset.step)).toEqual(trace.map((step) => step.step_id))
    expect(rows()).toHaveLength(trace.length)
    for (const [index, row] of rows().entries()) {
      expect(row).toHaveAttribute('id', `trace-step-${index}`)
      expect(row.parentElement?.tagName).toBe('OL')
      expect(row).not.toHaveAttribute('inert')
      expect(header(row)).toHaveAttribute('aria-expanded', 'false')
      expect(row.querySelector('[data-summary]')).not.toBeEmptyDOMElement()
      expect(details(row)).not.toBeVisible()
    }
    expect(screen.getAllByRole('heading', { level: 4 })).toHaveLength(trace.length)
    expect(screen.getAllByRole('heading', { level: 3 }).length).toBeGreaterThan(1)
    expect(trace).toEqual(before)
  })

  it('exposes each formula and source with keyboard disclosure, while leaving other rows compact', async () => {
    const user = userEvent.setup()
    show()
    const row = rows().find((candidate) => candidate.dataset.step === 'A')!
    const button = header(row)
    button.focus()
    await user.keyboard('{Enter}')
    expect(button).toHaveAttribute('aria-expanded', 'true')
    expect(details(row)).toBeVisible()
    const stored = steps.find((step) => step.step_id === 'A')!
    expect(within(details(row)).getByRole('img', { name: stored.expression })).toBeInTheDocument()
    expect(within(details(row)).getByText('Engineer rule')).toBeVisible()
    expect(rows().filter((candidate) => header(candidate).getAttribute('aria-expanded') === 'true')).toEqual([row])
    await user.keyboard(' ')
    expect(button).toHaveAttribute('aria-expanded', 'false')
    expect(details(row)).not.toBeVisible()
  })

  it('retains complete original fields and text check status through global expansion and collapse', () => {
    show()
    for (const row of rows()) {
      const stored = steps.find((step) => step.step_id === row.dataset.step)!
      if (stored.kind === 'check') expect(header(row)).toHaveTextContent(stored.passed ? 'Check passed' : 'Check failed')
    }
    fireEvent.click(screen.getByRole('button', { name: 'Expand all steps' }))
    for (const [index, row] of rows().entries()) {
      expect(header(row)).toHaveAttribute('aria-expanded', 'true')
      expect(details(row)).toBeVisible()
      expect(within(details(row)).getByRole('img', { name: steps[index].expression })).toBeInTheDocument()
      const list = details(row).querySelector('ul')
      if (steps[index].substitutions.length > 0) expect(list?.children).toHaveLength(steps[index].substitutions.length)
      if (steps[index].kind === 'engineer_formula') expect(within(details(row)).getByText('Engineer rule')).toBeVisible()
    }
    fireEvent.click(screen.getByRole('button', { name: 'Collapse all steps' }))
    expect(rows().every((row) => header(row).getAttribute('aria-expanded') === 'false')).toBe(true)
    expect(rows().map((row) => row.dataset.step)).toEqual(steps.map((step) => step.step_id))
  })

  it.each([
    passEnvelope.trace,
    steps.filter((step) => step.step_id !== 'Wx'),
    [...steps, steps.find((step) => step.step_id === 'Wx')!],
    steps.map((step) => step.step_id === 'Wx' ? { ...passEnvelope.trace[0], step_id: 'Wx' } : step),
  ].map((trace) => ({ trace })))('uses the existing expanded view for pilot or incomplete/ambiguous signatures', ({ trace }) => {
    show(trace)
    expect(rows().map((row) => row.dataset.step)).toEqual(trace.map((step) => step.step_id))
    expect(rows().every((row) => header(row).getAttribute('aria-expanded') === 'true')).toBe(true)
    expect(rows().every((row) => row.querySelector('[data-step-heading]')?.tagName === 'H3')).toBe(true)
    expect(document.querySelectorAll('[data-trace-section]')).toHaveLength(0)
  })

  it('keeps neutral supplemental runs and disjoint recognized runs in their original positions', () => {
    const unknown = { ...steps[0], step_id: 'unknown_recorded_step' }
    const trace = [steps[0], unknown, ...steps.slice(1)]
    show(trace)
    const headings = screen.getAllByRole('heading', { level: 3 })
    expect(headings[0].textContent).toBe(headings[2].textContent)
    expect(headings[1].textContent).not.toBe(headings[0].textContent)
    expect(rows()[1]).toHaveAttribute('data-step', unknown.step_id)
    fireEvent.click(header(rows()[1]))
    expect(details(rows()[1])).toBeVisible()
    expect(rows().map((row) => row.dataset.step)).toEqual(trace.map((step) => step.step_id))
  })

  it('preserves original arrival indices and disclosure choices when playback finishes', () => {
    const skip = vi.fn()
    const view = (phase: 'playing' | 'skipped', shown: number) => <I18nProvider initialLanguage="en"><Trace steps={steps} unverifiedStepCount={0} playback={{ phase, shown, skip }} /></I18nProvider>
    const { rerender } = render(view('playing', 2))
    expect(rows().slice(2).every((row) => row.hasAttribute('inert'))).toBe(true)
    expect(rows()[0]).not.toHaveAttribute('inert')
    for (const heading of document.querySelectorAll('[data-trace-section]')) {
      if (heading.closest('[data-step]') !== rows()[0]) expect(heading.closest('[data-step]')).toHaveAttribute('inert')
    }
    fireEvent.click(header(rows()[0]))
    rerender(view('skipped', steps.length))
    expect(header(rows()[0])).toHaveAttribute('aria-expanded', 'true')
    expect(header(rows()[1])).toHaveAttribute('aria-expanded', 'false')
    expect(rows().some((row) => row.hasAttribute('inert'))).toBe(false)
    expect(rows().every((row, index) => row.id === `trace-step-${index}`)).toBe(true)
  })

  it.each([false, true])('has no detectable accessibility violations with expanded details %s', async (expanded) => {
    const { container } = show()
    if (expanded) fireEvent.click(screen.getByRole('button', { name: 'Expand all steps' }))
    await expectNoA11yViolations(container)
  }, 10000)
})
