export type Language = 'ru' | 'en'

export const languages: readonly Language[] = ['ru', 'en']

export const ru = {
  'language.switch': 'Язык интерфейса',
  'language.ru': 'Русский',
  'language.en': 'English',
} as const

export type TextKey = keyof typeof ru

export type Dictionary = Readonly<Record<TextKey, string>>
export type PartialDictionary = Readonly<Partial<Record<TextKey, string>>>

export const en: PartialDictionary = {
  'language.switch': 'Interface language',
}

export interface Dictionaries {
  readonly ru: Dictionary
  readonly en: PartialDictionary
}

export const dictionaries: Dictionaries = { ru, en }
