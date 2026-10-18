import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { passEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { Outputs } from './Outputs'
import type { StampReveal } from './VerdictStamp'

type Output = components['schemas']['OutputValue']

const outputs = passEnvelope.outputs as unknown as Output[]
const [engineerSet] = outputs
function show(list: Output[], language: Language = 'ru', reveal: StampReveal = 'none') {
  return render(
    <I18nProvider initialLanguage={language}>
      <Outputs outputs={list} reveal={reveal} />
    </I18nProvider>,
  )
}

const rowOf = (quantity: string) => document.querySelector<HTMLElement>(`[data-output="${quantity}"]`)!
const itemOf = (quantity: string) => within(rowOf(quantity))
const reading = (quantity: string) =>
  `${rowOf(quantity).querySelector('[data-value]')!.textContent} ${rowOf(quantity).querySelector('[data-value]')!.nextElementSibling!.textContent}`

describe('Outputs (6.2)', () => {
  it('shows the value, the unit and the rounding rule, and no source of the rule', () => {
    show(outputs)
    const item = itemOf('R')

    expect(screen.getByRole('heading', { name: 'Выходные величины', level: 2 })).toBeInTheDocument()
    expect(reading('R')).toBe('172,5 кПа')
    expect(item.getByText('R')).toBeInTheDocument()
    expect(item.getByText(/Округление:/).parentElement).toHaveTextContent(
      'Округление: до ближайшего, половина вверх; знаков после запятой: 1',
    )
    expect(screen.getAllByRole('columnheader').map((header) => header.textContent)).toEqual([
      'Величина',
      'Значение',
      'Единица',
      'Округление',
    ])
    expect(screen.queryByText('Задано инженером')).not.toBeInTheDocument()
    expect(screen.queryByText('Источник правила')).not.toBeInTheDocument()
  })

  it('names the mode of the rule in words for both modes', () => {
    show([
      { ...engineerSet, quantity: 'A', rounding_rule: { decimals: 2, mode: 'half_up' } } as Output,
      { ...engineerSet, quantity: 'B', rounding_rule: { decimals: 0, mode: 'half_even' } } as Output,
    ])

    expect(itemOf('A').getByText(/Округление:/).parentElement).toHaveTextContent('до ближайшего, половина вверх; знаков после запятой: 2')
    expect(itemOf('B').getByText(/Округление:/).parentElement).toHaveTextContent('до ближайшего, половина к чётному; знаков после запятой: 0')
  })

  it('keeps the trailing zeros of the rule and changes no digit of the value', () => {
    show([
      { ...engineerSet, quantity: 'A', value: 172, rounding_rule: { decimals: 1, mode: 'half_up' } } as Output,
      { ...engineerSet, quantity: 'B', value: 172.456, rounding_rule: { decimals: 1, mode: 'half_up' } } as Output,
    ])

    expect(reading('A')).toBe('172,0 кПа')
    expect(reading('B')).toBe('172,456 кПа')
  })

  it('shows every output of the envelope', () => {
    show([engineerSet, { ...engineerSet, quantity: 'S' } as Output])

    expect(screen.getAllByRole('row')).toHaveLength(3)
    expect(itemOf('S').getByText('S')).toBeInTheDocument()
  })

  it('shows English texts, the English decimal point and unit codes', () => {
    show(outputs, 'en')
    const item = itemOf('R')

    expect(screen.getByRole('heading', { name: 'Outputs' })).toBeInTheDocument()
    expect(reading('R')).toBe('172.5 kPa')
    expect(item.getByText('Rounding:').parentElement).toHaveTextContent('to nearest, ties up; decimal places: 1')
  })

  it('shows a dash in the unit column for a dimensionless output, said in words', () => {
    show([{ ...engineerSet, quantity: 'k_z', unit: '1' }])
    const row = rowOf('k_z')

    expect(row).not.toHaveTextContent('безразм.')
    expect(within(row).getByText('—')).toHaveAttribute('aria-hidden', 'true')
    expect(within(row).getByText('безразмерная')).toHaveClass('sr-only')
  })

  it('has no accessibility violations', async () => {
    const { container } = show(outputs)

    await expectNoA11yViolations(container)
  })
})

describe('Outputs: held until the trace has played', () => {
  it('keeps the table in place with the values hidden from sight, focus and assistive technology', () => {
    show(outputs, 'ru', 'pending')
    const section = screen.getByRole('heading', { name: 'Выходные величины' }).closest('section')!

    expect(section).toHaveAttribute('data-reveal', 'pending')
    expect(section.className).toContain('outputs-pending')
    expect(section.querySelector('tbody')).toHaveAttribute('inert')
    expect(section.querySelector('[data-outputs-status]')).toHaveTextContent('ВЫПОЛНЕНИЕ РАСЧЁТА')
    expect(section.querySelector('[data-outputs-status]')).toHaveAttribute('aria-hidden', 'true')
  })

  it.each([
    ['celebrate', 'outputs-celebrate'],
    ['plain', ''],
    ['none', ''],
  ] as const)('shows the values once the reveal is %s', (reveal, className) => {
    show(outputs, 'ru', reveal)
    const section = screen.getByRole('heading', { name: 'Выходные величины' }).closest('section')!

    expect(section).toHaveAttribute('data-reveal', reveal)
    expect(section.querySelector('tbody')).not.toHaveAttribute('inert')
    expect(section.querySelector('[data-outputs-status]')).toBeNull()
    expect(section.className.includes('outputs-celebrate')).toBe(className !== '')
    expect(reading('R')).toBe('172,5 кПа')
  })

  it('has no accessibility violations while held', async () => {
    const { container } = show(outputs, 'ru', 'pending')

    await expectNoA11yViolations(container)
  })
})
