import type { Dictionaries, Language, TextKey } from './dictionary'

export function translate(
  dictionaries: Dictionaries,
  language: Language,
  key: TextKey,
): string {
  return dictionaries[language][key] ?? dictionaries.ru[key]
}

const locales: Readonly<Record<Language, string>> = { ru: 'ru-RU', en: 'en-US' }

export function formatNumber(value: number, language: Language): string {
  return new Intl.NumberFormat(locales[language], {
    maximumFractionDigits: 20,
    useGrouping: false,
  }).format(value)
}
