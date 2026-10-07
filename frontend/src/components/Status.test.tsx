import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { expectNoA11yViolations } from '@/test/axe'
import { Status, type StatusTone } from './Status'

function show(tone: StatusTone, language: Language = 'ru') {
  return render(
    <I18nProvider initialLanguage={language}>
      <Status tone={tone} title="заголовок">
        <p>подробности</p>
      </Status>
    </I18nProvider>,
  )
}

function stripStyles(container: HTMLElement) {
  container.querySelectorAll('[class], [style]').forEach((element) => {
    element.removeAttribute('class')
    element.removeAttribute('style')
  })
  container.querySelectorAll('svg').forEach((icon) => icon.remove())
}

describe('Status (6.4a)', () => {
  it.each([
    ['warning', 'Предупреждение'],
    ['refusal', 'Расчёт не выполнен'],
  ] as const)('carries the meaning of a %s in text with every style and the icon removed', (tone, label) => {
    const { container } = show(tone)

    stripStyles(container)

    expect(container).toHaveTextContent(`${label}: заголовок`)
    expect(screen.getByRole('region', { name: `${label}: заголовок` })).toHaveTextContent('подробности')
  })

  it('gives the warning and the refusal different frames and icons hidden from assistive technology', () => {
    const { container } = show('warning')
    const warning = container.querySelector('[data-status="warning"]')!
    const { container: other } = show('refusal')
    const refusal = other.querySelector('[data-status="refusal"]')!

    expect(warning.className).toContain('border-dashed')
    expect(refusal.className).toContain('border-double')
    expect([warning, refusal].map((frame) => frame.querySelector('svg')?.getAttribute('aria-hidden'))).toEqual([
      'true',
      'true',
    ])
  })

  it('speaks English with the language switched', () => {
    show('refusal', 'en')

    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Calculation refused: заголовок')
  })

  it.each(['warning', 'refusal'] as const)('has no axe violation as a %s', async (tone) => {
    const { container } = show(tone)

    await expectNoA11yViolations(container)
  })
})
