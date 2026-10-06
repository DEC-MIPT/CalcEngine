import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { LanguageSwitch } from '@/components/LanguageSwitch'
import { useI18n } from './context'
import { en, ru } from './dictionary'
import { I18nProvider } from './I18nProvider'
import { formatNumber, pickText, translate } from './translate'

describe('translate', () => {
  it('uses the English text when it exists', () => {
    expect(translate({ ru, en }, 'en', 'language.switch')).toBe('Interface language')
  })

  it('falls back to the Russian text when an English key is missing', () => {
    expect(translate({ ru, en }, 'en', 'language.ru')).toBe('Русский')
  })

  it('shows the Russian text in Russian', () => {
    expect(translate({ ru, en }, 'ru', 'language.switch')).toBe('Язык интерфейса')
  })
})

describe('formatNumber', () => {
  it('uses a decimal comma in Russian and a point in English', () => {
    expect(formatNumber(172.5, 'ru')).toBe('172,5')
    expect(formatNumber(172.5, 'en')).toBe('172.5')
  })

  it('keeps trailing zeros up to the minimum and never cuts further digits', () => {
    expect(formatNumber(172, 'ru', 1)).toBe('172,0')
    expect(formatNumber(172.456, 'en', 1)).toBe('172.456')
  })

  it('does not round or group the value', () => {
    expect(formatNumber(1234567.123456, 'en')).toBe('1234567.123456')
  })
})

function Probe() {
  const { formatNumber: format, t } = useI18n()
  return (
    <p>
      {t('language.switch')} {format(172.5)}
    </p>
  )
}

describe('I18nProvider and LanguageSwitch', () => {
  it('starts in Russian and sets the document language', () => {
    render(
      <I18nProvider>
        <Probe />
      </I18nProvider>,
    )
    expect(screen.getByText('Язык интерфейса 172,5')).toBeInTheDocument()
    expect(document.documentElement.lang).toBe('ru')
  })

  it('switches the texts, the numbers and the document language', () => {
    render(
      <I18nProvider>
        <LanguageSwitch />
        <Probe />
      </I18nProvider>,
    )
    fireEvent.click(screen.getByRole('button', { name: 'English' }))
    expect(screen.getByText('Interface language 172.5')).toBeInTheDocument()
    expect(document.documentElement.lang).toBe('en')
    expect(screen.getByRole('button', { name: 'English' })).toHaveAttribute(
      'aria-pressed',
      'true',
    )
    expect(screen.getByRole('button', { name: 'Русский' })).toHaveAttribute(
      'aria-pressed',
      'false',
    )
  })

  it('accepts an initial language', () => {
    render(
      <I18nProvider initialLanguage="en">
        <Probe />
      </I18nProvider>,
    )
    expect(screen.getByText('Interface language 172.5')).toBeInTheDocument()
  })

  it('refuses to be used outside the provider', () => {
    expect(() => render(<Probe />)).toThrow('useI18n must be used inside I18nProvider')
  })
})

describe('pickText', () => {
  const text = { ru: 'Ширина', en: 'Width' }

  it('picks the text of the language', () => {
    expect(pickText(text, 'ru')).toBe('Ширина')
    expect(pickText(text, 'en')).toBe('Width')
  })

  it('falls back to Russian when the English text is missing or empty', () => {
    expect(pickText({ ru: 'Ширина' }, 'en')).toBe('Ширина')
    expect(pickText({ ru: 'Ширина', en: null }, 'en')).toBe('Ширина')
    expect(pickText({ ru: 'Ширина', en: '' }, 'en')).toBe('Ширина')
  })
})
