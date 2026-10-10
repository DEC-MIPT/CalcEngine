import { render } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { expectNoA11yViolations } from '@/test/axe'
import { QuantityText, UnitText } from './Quantity'

function show(node: React.ReactNode, language: Language = 'ru') {
  return render(<I18nProvider initialLanguage={language}>{node}</I18nProvider>)
}

describe('QuantityText', () => {
  it('writes the value with its unit', () => {
    const { container } = show(<QuantityText value={172.5} unit="kPa" />)

    expect(container.textContent).toBe('172,5 кПа')
  })

  it.each(['ru', 'en'] as const)('writes a dimensionless value as a bare number in %s', (language) => {
    const { container } = show(<QuantityText value={0.5} unit="1" />, language)

    expect(container.textContent).toBe(language === 'ru' ? '0,5' : '0.5')
  })

  it('wraps the unit in its own element when it is styled', () => {
    const { container } = show(<QuantityText value={2} unit="m" unitClassName="text-muted-foreground" />)

    expect(container.querySelector('span.text-muted-foreground')).toHaveTextContent('м')
    expect(container.textContent).toBe('2 м')
  })
})

describe('UnitText', () => {
  it('names a unit by its designation', () => {
    const { container } = show(<UnitText unit="kN/m3" />)

    expect(container.textContent).toBe('кН/м³')
  })

  it('shows a dash for a dimensionless quantity and says it in words', async () => {
    const { container } = show(<UnitText unit="1" />, 'en')

    expect(container.querySelector('[aria-hidden="true"]')).toHaveTextContent('—')
    expect(container.querySelector('.sr-only')).toHaveTextContent('dimensionless')
    await expectNoA11yViolations(container)
  })
})
