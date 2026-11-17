import type { Dictionaries, Language, TextKey } from './dictionary'

export function translate(
  dictionaries: Dictionaries,
  language: Language,
  key: TextKey,
): string {
  return dictionaries[language][key] ?? dictionaries.ru[key]
}

const locales: Readonly<Record<Language, string>> = { ru: 'ru-RU', en: 'en-US' }
const MAX_FRACTION_DIGITS = 20

export function formatNumber(value: number, language: Language, minimumFractionDigits = 0): string {
  if (minimumFractionDigits === 0 && value !== 0 && Math.abs(value) < 10 ** -MAX_FRACTION_DIGITS) {
    return new Intl.NumberFormat(locales[language], {
      notation: 'scientific',
      maximumSignificantDigits: 21,
      useGrouping: false,
    }).format(value)
  }
  return new Intl.NumberFormat(locales[language], {
    minimumFractionDigits,
    maximumFractionDigits: MAX_FRACTION_DIGITS,
    useGrouping: false,
  }).format(value)
}

export function pickText(text: { ru: string; en?: string | null }, language: Language): string {
  return language === 'en' && text.en ? text.en : text.ru
}
