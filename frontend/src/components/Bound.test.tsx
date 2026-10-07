import { render } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { BoundFacts } from './Bound'

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
