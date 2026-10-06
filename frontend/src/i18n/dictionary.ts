export type Language = 'ru' | 'en'

export const languages: readonly Language[] = ['ru', 'en']

export const ru = {
  'language.switch': 'Язык интерфейса',
  'language.ru': 'Русский',
  'language.en': 'English',
  'app.title': 'Калькулятор инженера-проектировщика',
  'nav.types': 'Типы расчётов',
  'nav.main': 'Основная навигация',
  'state.loading': 'Загрузка…',
  'state.unavailable': 'Расчёт сейчас недоступен.',
  'state.failed': 'Не удалось выполнить запрос.',
  'state.code': 'Код ошибки',
  'state.retry': 'Повторить',
  'types.title': 'Выберите тип расчёта',
  'types.empty': 'Нет доступных типов расчёта.',
  'notFound.page': 'Страница не найдена',
  'notFound.result': 'Результат не найден',
  'notFound.toTypes': 'К выбору типа расчёта',
} as const

export type TextKey = keyof typeof ru

export type Dictionary = Readonly<Record<TextKey, string>>
export type PartialDictionary = Readonly<Partial<Record<TextKey, string>>>

export const en: PartialDictionary = {
  'language.switch': 'Interface language',
  'app.title': "Design Engineer's Calculator",
  'nav.types': 'Calculation types',
  'nav.main': 'Main navigation',
  'state.loading': 'Loading…',
  'state.unavailable': 'The calculation is not available now.',
  'state.failed': 'The request failed.',
  'state.code': 'Error code',
  'state.retry': 'Retry',
  'types.title': 'Choose a calculation type',
  'types.empty': 'No calculation types are available.',
  'notFound.page': 'Page not found',
  'notFound.result': 'Result not found',
  'notFound.toTypes': 'Back to the choice of calculation type',
}

export interface Dictionaries {
  readonly ru: Dictionary
  readonly en: PartialDictionary
}

export const dictionaries: Dictionaries = { ru, en }
