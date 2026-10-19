import { fireEvent, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { components } from '@/api/schema'
import type { TracePlayback } from '@/lib/useTracePlayback'
import { passEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { TraceRuler } from './TraceRuler'

type Step = components['schemas']['ResultEnvelope']['trace'][number]

const steps = passEnvelope.trace as unknown as Step[]
const ticks = () => [...document.querySelectorAll<HTMLAnchorElement>('[data-tick]')]
const scrollIntoView = vi.fn()

beforeEach(() => {
  Element.prototype.scrollIntoView = scrollIntoView
})

afterEach(() => {
  scrollIntoView.mockReset()
  delete (Element.prototype as Partial<Element>).scrollIntoView
})

describe('TraceRuler', () => {
  it('draws a bare rule with no ticks and no verdict while there is no trace', () => {
    render(<TraceRuler />)

    const ruler = document.querySelector('[data-ruler]')!
    expect(ruler).toHaveAttribute('data-ruler', '0')
    expect(ruler).toHaveAttribute('aria-hidden', 'true')
    expect(ticks()).toHaveLength(0)
    expect(document.querySelector('[data-ruler-verdict]')).toBeNull()
  })

  it('puts one tick per step, named by the step and linked to it, out of the tab order', () => {
    render(<TraceRuler steps={steps} verdict="pass" />)

    expect(ticks()).toHaveLength(steps.length)
    ticks().forEach((tick, index) => {
      expect(tick).toHaveAttribute('href', `#trace-step-${index}`)
      expect(tick).toHaveAttribute('tabindex', '-1')
      expect(tick).toHaveTextContent(steps[index].step_id)
      expect(tick).toHaveAttribute('data-arrival', 'shown')
    })
    expect(document.querySelector('[data-ruler-cursor]')).toBeNull()
  })

  it('names a tick by the symbol of its step, the given symbols first, and by the id when there is none', () => {
    const named = [
      { ...steps[0], step_id: 'gamma_c1', expression: '\\gamma_{c1}' },
      { ...steps[0], step_id: 'M_gamma', expression: 'M_{\\gamma} = M_{\\gamma}\\left(x\\right)' },
      { ...steps[0], step_id: 'q', kind: 'formula', expression: '\\frac{a}{b}' },
    ] as unknown as Step[]
    render(<TraceRuler steps={named} verdict="pass" symbols={new Map([['M_gamma', 'M_\\gamma']])} />)

    const labels = ticks().map((tick) => tick.querySelector<HTMLElement>('.tr-label')!)
    expect(labels.map((label) => label.querySelector('[role="img"]')?.getAttribute('aria-label') ?? null)).toEqual([
      null,
      'M_\\gamma',
      null,
    ])
    expect(labels.map((label) => label.querySelector('code')?.textContent ?? null)).toEqual(['gamma_c1', null, 'q'])
  })

  it('reads the symbols from the steps when none are given', () => {
    render(<TraceRuler steps={[{ ...steps[0], expression: '\\gamma_{c1}' } as Step]} verdict="pass" />)

    expect(document.querySelector('.tr-label [role="img"]')).toHaveAttribute('aria-label', '\\gamma_{c1}')
  })

  it.each(['pass', 'fail'] as const)('ends with the mark of a %s verdict', (verdict) => {
    render(<TraceRuler steps={steps} verdict={verdict} />)

    expect(document.querySelector('[data-ruler-verdict]')).toHaveAttribute('data-ruler-verdict', verdict)
    expect(document.querySelector(`[data-mark="${verdict}"]`)).toBeInTheDocument()
  })

  it('draws the ticks as the steps arrive, with the cursor at the last one and no verdict yet', () => {
    const playback: TracePlayback = { phase: 'playing', shown: 3, skip: vi.fn() }
    render(<TraceRuler steps={steps} verdict="pass" playback={playback} reveal="pending" />)

    expect(ticks().map((tick) => tick.dataset.arrival)).toEqual([
      'reveal',
      'reveal',
      'reveal',
      ...Array(steps.length - 3).fill('pending'),
    ])
    expect(ticks()[3].className).toContain('tr-pending')
    expect(document.querySelector<HTMLElement>('[data-ruler-cursor]')!.style.getPropertyValue('--at')).toBe('3')
    expect(document.querySelector('[data-ruler-verdict]')).toBeNull()
  })

  it('marks the celebrated verdict for its drawn mark', () => {
    render(<TraceRuler steps={steps} verdict="pass" reveal="celebrate" />)

    expect(document.querySelector('[data-ruler]')!.className).toContain('tr-celebrate')
  })

  it('skips the playback and jumps to the step on a click while playing', () => {
    const skip = vi.fn()
    render(
      <>
        <TraceRuler steps={steps} verdict="pass" playback={{ phase: 'playing', shown: 1, skip }} reveal="pending" />
        <ol>
          {steps.map((step, index) => (
            <li key={index} id={`trace-step-${index}`}>
              {step.step_id}
            </li>
          ))}
        </ol>
      </>,
    )

    const followed = fireEvent.click(ticks()[5])

    expect(skip).toHaveBeenCalledTimes(1)
    expect(followed).toBe(false)
    expect(scrollIntoView).toHaveBeenCalledTimes(1)
    expect(scrollIntoView.mock.contexts[0]).toBe(document.getElementById('trace-step-5'))
  })

  it('only jumps once the playback is over', () => {
    const skip = vi.fn()
    render(
      <>
        <TraceRuler steps={steps} verdict="pass" playback={{ phase: 'ended', shown: steps.length, skip }} />
        <p id="trace-step-0">first</p>
      </>,
    )

    fireEvent.click(ticks()[0])

    expect(skip).not.toHaveBeenCalled()
    expect(scrollIntoView).toHaveBeenCalledTimes(1)
  })

  it('has no accessibility violations', async () => {
    const { container } = render(<TraceRuler steps={steps} verdict="fail" />)

    await expectNoA11yViolations(container)
  })
})
