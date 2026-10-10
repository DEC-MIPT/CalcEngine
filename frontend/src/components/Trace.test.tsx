import { fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { failEnvelope, passEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { Trace } from './Trace'

type Step = components['schemas']['ResultEnvelope']['trace'][number]

const steps = passEnvelope.trace as unknown as Step[]
const formula = steps.find((step) => step.kind === 'formula' && step.substitutions.length > 0)!
const ref = {
  document: 'SP Test',
  edition: '2020',
  clause: '5.6',
  status: 'verified',
  provenance: 'human-verified',
} as const

const EXPAND_ALL = { ru: 'Развернуть все шаги', en: 'Expand all steps' } as const

function show(trace: Step[], language: Language = 'ru', unverifiedStepCount = 0, expand = true) {
  const rendered = render(
    <I18nProvider initialLanguage={language}>
      <Trace steps={trace} unverifiedStepCount={unverifiedStepCount} />
    </I18nProvider>,
  )
  if (expand) fireEvent.click(screen.getByRole('button', { name: EXPAND_ALL[language] }))
  return rendered
}

const stepOf = (id: string) => document.querySelector<HTMLElement>(`[data-step="${id}"]`)!

describe('Trace: every field of a step (6.1a)', () => {
  it('shows every step of the envelope in order', () => {
    show(steps)

    expect(screen.getByRole('heading', { name: 'Ход расчёта', level: 2 })).toBeInTheDocument()
    expect(screen.getAllByRole('heading', { level: 3 }).map((heading) => heading.querySelector('code')?.textContent)).toEqual(
      steps.map((step) => step.step_id),
    )
  })

  it('shows the expression typeset, the substitutions with units, the result with its unit and the norm refs', () => {
    show(steps)
    const step = within(stepOf(formula.step_id))

    expect(step.getAllByRole('img', { name: formula.expression }).length).toBeGreaterThan(0)
    for (const substitution of formula.substitutions) {
      expect(step.getByRole('img', { name: substitution.symbol })).toBeInTheDocument()
    }
    const list = step.getByRole('heading', { name: 'Подстановка' }).nextElementSibling as HTMLElement
    expect(list.children).toHaveLength(formula.substitutions.length)
    expect(list).toHaveTextContent('= 2 м')
    expect(list).toHaveTextContent('= 10 кН/м³')
    expect(list).toHaveTextContent('= 3 кПа')
    expect(step.getByText(/Результат:/).parentElement).toHaveTextContent('Результат: 172,5 кПа')
    expect(step.getByText('<NORM-DOC-PLACEHOLDER>')).toBeInTheDocument()
    expect(step.getByText('пункт: <CLAUSE-PLACEHOLDER>')).toBeInTheDocument()
  })

  it('shows the kind of each step in words', () => {
    show(steps)

    expect(within(stepOf('gamma_c1')).getByText('Значение из таблицы')).toBeInTheDocument()
    expect(within(stepOf('R')).getByText('Формула')).toBeInTheDocument()
    expect(within(stepOf('p_le_R')).getByText('Проверка')).toBeInTheDocument()
  })

  it('shows a dimensionless result as a bare number and a step with nothing to substitute without an empty block', () => {
    show(steps)

    const result = within(stepOf('gamma_c1')).getByText(/Результат:/).parentElement!
    expect(result.textContent).toBe('Результат: 2')
    expect(stepOf('gamma_c1').querySelector('[data-summary]')!.textContent).toBe('2')
    expect(within(stepOf('gamma_c1')).queryByText('Подстановка')).not.toBeInTheDocument()
  })

  it('shows English texts and unit codes in English', () => {
    show(steps, 'en')

    expect(within(stepOf('R')).getByText('Result:').parentElement).toHaveTextContent('Result: 172.5 kPa')
    expect(within(stepOf('R')).getByText('Substitution')).toBeInTheDocument()
  })

  it('has no accessibility violations', async () => {
    const { container } = show(steps)

    await expectNoA11yViolations(container)
  })
})

describe('Trace: norm reference status (6.1a)', () => {
  const withRefs = (...refs: (typeof ref | Record<string, string>)[]) => [
    { ...formula, norm_refs: refs } as unknown as Step,
  ]

  it('shows an unverified reference as unverified and never as verified', () => {
    show(steps)

    for (const step of steps) {
      expect(within(stepOf(step.step_id)).queryByText('проверено')).not.toBeInTheDocument()
      expect(within(stepOf(step.step_id)).getAllByText('не проверено').length).toBeGreaterThan(0)
    }
  })

  it('shows the status of the reference as it is, also when the provenance is human-verified', () => {
    show(withRefs({ ...ref, status: 'unverified' }, ref))

    const step = within(stepOf(formula.step_id))
    expect(step.getAllByText('не проверено')).toHaveLength(1)
    expect(step.getAllByText('проверено')).toHaveLength(1)
  })

  it('shows document, edition and clause exactly as recorded, and the word for an unverified edition', () => {
    show(withRefs(ref, { ...ref, document: 'SP Other', edition: 'unverified', clause: '7.1', status: 'unverified' }))

    const items = within(stepOf(formula.step_id)).getAllByRole('listitem').filter((item) => item.textContent?.includes('SP '))
    expect(items[0]).toHaveTextContent('SP Test редакция: 2020 пункт: 5.6 проверено')
    expect(items[1]).toHaveTextContent('SP Other редакция: не подтверждена пункт: 7.1 не проверено')
  })

  it('says that an unrecorded clause is not confirmed, apart from the verification status', () => {
    show(withRefs({ ...ref, clause: 'unverified', status: 'unverified' }))

    const item = within(stepOf(formula.step_id)).getAllByRole('listitem').find((entry) => entry.textContent?.includes('SP Test'))!
    expect(item).toHaveTextContent('SP Test редакция: 2020 пункт: не подтверждён не проверено')
  })

  it('shows no block of references for a step without any', () => {
    show(withRefs())

    expect(within(stepOf(formula.step_id)).queryByText('Нормативные ссылки')).not.toBeInTheDocument()
  })
})

describe('Trace: check steps and the unverified summary (6.1b)', () => {
  const check = steps.find((step) => step.kind === 'check') as Extract<Step, { kind: 'check' }>

  it('says in words that a check passed and shows both values with units', () => {
    show(steps)
    const step = within(stepOf(check.step_id))

    expect(step.getByText('Проверка выполнена')).toBeInTheDocument()
    expect(step.getByText('меньше или равно')).toBeInTheDocument()
    const comparison = step.getByText('Проверка выполнена').previousElementSibling as HTMLElement
    expect(comparison).toHaveTextContent('100 кПа ≤ меньше или равно 172,5 кПа')
    expect(step.queryByText(/Результат:/)).not.toBeInTheDocument()
  })

  it('says in words that a check failed', () => {
    const failed = (failEnvelope.trace as unknown as Step[]).find((step) => step.kind === 'check')!
    show([failed])

    const step = within(stepOf(failed.step_id))
    expect(step.getByText('Проверка не выполнена')).toBeInTheDocument()
    expect(step.queryByText('Проверка выполнена')).not.toBeInTheDocument()
  })

  it.each([
    ['le', '≤', 'меньше или равно'],
    ['lt', '<', 'меньше'],
    ['ge', '≥', 'больше или равно'],
    ['gt', '>', 'больше'],
  ] as const)('shows the operator %s as a symbol and in words', (operator, symbol, words) => {
    show([{ ...check, operator } as Step])

    const step = within(stepOf(check.step_id))
    expect(step.getByText(words)).toBeInTheDocument()
    expect(step.getByText(symbol)).toHaveAttribute('aria-hidden', 'true')
  })

  it('shows the same words in English', () => {
    show(steps, 'en')

    expect(within(stepOf(check.step_id)).getByText('Check passed')).toBeInTheDocument()
    expect(within(stepOf(check.step_id)).getByText('less than or equal to')).toBeInTheDocument()
  })

  it('shows the count of unverified steps above the trace when it is above zero', () => {
    show(steps, 'ru', 9)

    const summary = screen.getByText('Шагов с непроверенными нормативными ссылками', { exact: false })
    expect(summary).toHaveTextContent('Шагов с непроверенными нормативными ссылками: 9')
    const list = screen.getAllByRole('list').find((candidate) => candidate.tagName === 'OL')!
    expect(summary.compareDocumentPosition(list) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('shows no summary at zero', () => {
    show(steps, 'ru', 0)

    expect(screen.queryByText('Шагов с непроверенными нормативными ссылками', { exact: false })).not.toBeInTheDocument()
  })

  it('has no accessibility violations with a summary and a failed check', async () => {
    const failedTrace = failEnvelope.trace as unknown as Step[]
    const { container } = show(failedTrace, 'ru', 9)

    await expectNoA11yViolations(container)
  })
})


const check = steps.find((step) => step.kind === 'check')!
const header = (id: string) => within(stepOf(id)).getByRole('button')
const details = (id: string) => document.getElementById(header(id).getAttribute('aria-controls')!)!

describe('Trace: expandable steps (6.3)', () => {
  it('opens with every step expanded and its header showing the result with its unit', () => {
    show(steps, 'ru', 0, false)

    expect(screen.getAllByRole('button', { expanded: true })).toHaveLength(steps.length)
    for (const step of steps) {
      expect(details(step.step_id)).toBeVisible()
    }
    expect(header(formula.step_id).querySelector('[data-summary]')).toHaveTextContent('172,5 кПа')
    expect(header(check.step_id).querySelector('[data-summary]')).toHaveTextContent('100 кПа · Проверка выполнена')
  })

  it('collapses a step on a click, expands it on a second click, and points the header at its details', () => {
    show(steps, 'ru', 0, false)
    const button = header(formula.step_id)

    fireEvent.click(button)
    expect(button).toHaveAttribute('aria-expanded', 'false')
    expect(details(formula.step_id)).not.toBeVisible()

    fireEvent.click(button)
    expect(button).toHaveAttribute('aria-expanded', 'true')
    expect(details(formula.step_id)).toBeVisible()
    expect(within(details(formula.step_id)).getByText(/Результат:/)).toBeInTheDocument()
  })

  it('collapses and expands a step with Enter and with Space', async () => {
    const user = userEvent.setup()
    show(steps, 'ru', 0, false)
    const button = header(check.step_id)
    button.focus()

    await user.keyboard('{Enter}')
    expect(button).toHaveAttribute('aria-expanded', 'false')
    expect(details(check.step_id)).not.toBeVisible()

    await user.keyboard(' ')
    expect(button).toHaveAttribute('aria-expanded', 'true')
    expect(details(check.step_id)).toBeVisible()
  })

  it('reaches the step headers with the Tab key', async () => {
    const user = userEvent.setup()
    show(steps, 'ru', 0, false)

    await user.tab()
    await user.tab()
    await user.tab()

    expect(header(steps[0].step_id)).toHaveFocus()
  })

  it('collapses every step and expands every step with the two buttons', () => {
    show(steps, 'ru', 0, false)

    fireEvent.click(screen.getByRole('button', { name: 'Свернуть все шаги' }))
    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(steps.length)

    fireEvent.click(screen.getByRole('button', { name: 'Развернуть все шаги' }))
    expect(screen.getAllByRole('button', { expanded: true })).toHaveLength(steps.length)
  })

  it('gives each step an anchor by its position', () => {
    show(steps, 'ru', 0, false)

    expect(document.getElementById('trace-step-0')).toHaveAttribute('data-step', steps[0].step_id)
    expect(document.getElementById(`trace-step-${steps.length - 1}`)).toHaveAttribute('data-step', check.step_id)
  })

  it('keeps the other steps as they are when one is toggled after expanding all', () => {
    show(steps)

    fireEvent.click(header(formula.step_id))

    expect(header(formula.step_id)).toHaveAttribute('aria-expanded', 'false')
    expect(screen.getAllByRole('button', { expanded: true })).toHaveLength(steps.length - 1)
  })

  it('names the two buttons in English', () => {
    show(steps, 'en', 0, false)

    expect(screen.getByRole('button', { name: 'Expand all steps' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Collapse all steps' })).toBeInTheDocument()
  })

  it('has no accessibility violations collapsed', async () => {
    const { container } = show(steps, 'ru', 0, false)
    fireEvent.click(screen.getByRole('button', { name: 'Свернуть все шаги' }))

    await expectNoA11yViolations(container)
  })
})

describe('Trace: step-by-step playback', () => {
  function play(phase: 'playing' | 'ended' | 'skipped', shown: number, skip = vi.fn()) {
    render(
      <I18nProvider initialLanguage="ru">
        <Trace steps={steps} unverifiedStepCount={0} playback={{ phase, shown, skip }} />
      </I18nProvider>,
    )
    return skip
  }

  const arrivals = () => [...document.querySelectorAll('[data-step]')].map((step) => step.getAttribute('data-arrival'))

  it('keeps the steps not yet shown inert and out of the tab order', () => {
    play('playing', 2)

    expect(arrivals()).toEqual(['reveal', 'reveal', ...Array(steps.length - 2).fill('pending')])
    const pending = document.querySelectorAll<HTMLElement>('[data-arrival="pending"]')
    for (const step of pending) {
      expect(step).toHaveAttribute('inert')
      expect(step.className).toContain('step-pending')
    }
    expect(stepOf(steps[0].step_id)).not.toHaveAttribute('inert')
    expect(stepOf(steps[0].step_id).className).toContain('step-reveal')
  })

  it('shows the progress and the way to skip while playing', () => {
    play('playing', 3)

    const hint = document.querySelector('[data-skip-hint]')!
    expect(hint).toHaveAttribute('aria-hidden', 'true')
    expect(hint).toHaveTextContent(`трасса 3/${steps.length}`)
    expect(hint).toHaveTextContent('пробел или щелчок — показать всё')
  })

  it('pads the counter to the width of the total', () => {
    render(
      <I18nProvider initialLanguage="ru">
        <Trace steps={[...steps, ...steps]} unverifiedStepCount={0} playback={{ phase: 'playing', shown: 3, skip: vi.fn() }} />
      </I18nProvider>,
    )

    expect(document.querySelector('[data-skip-hint]')).toHaveTextContent(`03/${steps.length * 2}`)
  })

  it('skips on a click anywhere in the trace', () => {
    const skip = play('playing', 1)

    fireEvent.click(screen.getByRole('heading', { name: 'Ход расчёта' }))

    expect(skip).toHaveBeenCalledTimes(1)
  })

  it('does not listen to clicks once the playback is over', () => {
    const skip = play('ended', steps.length)

    fireEvent.click(screen.getByRole('heading', { name: 'Ход расчёта' }))

    expect(skip).not.toHaveBeenCalled()
    expect(document.querySelector('[data-skip-hint]')).toBeNull()
    expect(arrivals().every((arrival) => arrival === 'reveal')).toBe(true)
  })

  it('shows every step without the reveal after a skip', () => {
    play('skipped', steps.length)

    expect(arrivals().every((arrival) => arrival === 'shown')).toBe(true)
    expect(document.querySelector('.step-reveal')).toBeNull()
  })

  it('reports no accessibility violation while playing', async () => {
    const { container } = render(
      <I18nProvider initialLanguage="ru">
        <Trace steps={steps} unverifiedStepCount={0} playback={{ phase: 'playing', shown: 2, skip: vi.fn() }} />
      </I18nProvider>,
    )

    await expectNoA11yViolations(container)
  })
})
