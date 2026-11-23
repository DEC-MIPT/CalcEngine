import { render } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { DemoResultDisplay } from '@/lib/resultDisplay'
import { BoundFacts, BoundNote } from './Bound'

function bound(kind: 'min' | 'max', inclusive: boolean) {
  const { container } = render(
    <I18nProvider initialLanguage="ru">
      <BoundFacts
        value={{ value: 2.5, unit: 'm' }}
        bound={{ quantity: 'b', kind, value: 1, inclusive }}
        boundLabel="Граница"
      />
    </I18nProvider>,
  )
  return container.querySelector('[data-fact="bound"]')
}

describe('BoundFacts (6.4b, 6.4c)', () => {
  it.each([
    ['max', true, '≤меньше или равно'],
    ['max', false, '<меньше'],
    ['min', true, '≥больше или равно'],
    ['min', false, '>больше'],
  ] as const)('writes a %s bound (inclusive: %s) with its symbol and its words', (kind, inclusive, operator) => {
    expect(bound(kind, inclusive)).toHaveTextContent(`b ${operator} 1 м`)
  })
})

describe('BoundNote (9.2b)', () => {
  it.each([
    ['max', true, '≤меньше или равно'],
    ['max', false, '<меньше'],
    ['min', true, '≥больше или равно'],
    ['min', false, '>больше'],
  ] as const)('writes a %s bound (inclusive: %s) next to a field with its symbol and its words', (kind, inclusive, operator) => {
    const { container } = render(
      <I18nProvider initialLanguage="ru">
        <BoundNote id="note" bound={{ quantity: 'b', kind, value: 1, inclusive }} unit="m" />
      </I18nProvider>,
    )

    expect(container.querySelector('#note')).toHaveTextContent(`Метод допускает: b ${operator} 1 м`)
  })
})


it.each([[1.1, '1,10 м', '1,00 м'], [1.001, '1,001 м', '1 м']] as const)(
  'rounds a demo bound and its value only if the comparison is preserved for %s', (value, input, limit) => {
    const { container } = render(<I18nProvider><DemoResultDisplay.Provider value>
      <BoundFacts value={{ value, unit: 'm' }} bound={{ quantity: 'b', kind: 'max', value: 1, inclusive: true }} boundLabel="Граница" />
    </DemoResultDisplay.Provider></I18nProvider>)
    expect(container.querySelector('[data-fact="input"]')).toHaveTextContent(`b = ${input}`)
    expect(container.querySelector('[data-fact="bound"]')).toHaveTextContent(`b ≤меньше или равно ${limit}`)
  },
)
