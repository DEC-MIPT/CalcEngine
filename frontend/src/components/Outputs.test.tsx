import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { passEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { Outputs } from './Outputs'

type Output = components['schemas']['OutputValue']

const outputs = passEnvelope.outputs as unknown as Output[]
const [engineerSet] = outputs
const normRef = {
  document: 'SP Test',
  edition: '2020',
  clause: '5.6',
  status: 'verified',
  provenance: 'human-verified',
} as const

function show(list: Output[], language: Language = 'ru') {
  return render(
    <I18nProvider initialLanguage={language}>
      <Outputs outputs={list} />
    </I18nProvider>,
  )
}

const rowOf = (quantity: string) => document.querySelector<HTMLElement>(`[data-output="${quantity}"]`)!
const itemOf = (quantity: string) => within(rowOf(quantity))
const reading = (quantity: string) =>
  `${rowOf(quantity).querySelector('[data-value]')!.textContent} ${rowOf(quantity).querySelector('[data-value]')!.nextElementSibling!.textContent}`

describe('Outputs (6.2)', () => {
  it('shows the value, the unit, the rounding rule and the source of an engineer-set rule', () => {
    show(outputs)
    const item = itemOf('R')

    expect(screen.getByRole('heading', { name: 'Выходные величины', level: 2 })).toBeInTheDocument()
    expect(reading('R')).toBe('172,5 кПа')
    expect(item.getByText('R')).toBeInTheDocument()
    expect(item.getByText(/Округление:/).parentElement).toHaveTextContent(
      'Округление: до ближайшего, половина вверх; знаков после запятой: 1',
    )
    expect(item.getByText('Задано инженером')).toBeInTheDocument()
    expect(item.getByText('Инженер: <ENGINEER>')).toBeInTheDocument()
    expect(item.getByText('Обоснование: <RATIONALE>')).toBeInTheDocument()
  })

  it('shows a rule taken from a norm with its reference and no engineer', () => {
    show([{ ...engineerSet, rounding_source: [normRef] } as Output])
    const item = itemOf('R')

    expect(item.getByText('SP Test')).toBeInTheDocument()
    expect(item.getByText('редакция: 2020')).toBeInTheDocument()
    expect(item.getByText('пункт: 5.6')).toBeInTheDocument()
    expect(item.getByText('проверено')).toBeInTheDocument()
    expect(item.queryByText('Задано инженером')).not.toBeInTheDocument()
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
    expect(item.getByText('Set by the engineer')).toBeInTheDocument()
    expect(item.getByText('Rounding:').parentElement).toHaveTextContent('to nearest, ties up; decimal places: 1')
  })

  it('has no accessibility violations', async () => {
    const { container } = show(outputs)

    await expectNoA11yViolations(container)
  })
})
