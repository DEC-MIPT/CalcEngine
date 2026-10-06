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
  'form.title': 'Исходные данные',
  'form.unit': 'Единица',
  'form.submit': 'Рассчитать',
  'form.submitting': 'Расчёт…',
  'form.rejected': 'Запрос отклонён',
  'form.error.empty': 'Введите значение.',
  'form.error.notNumber': 'Введите число.',
  'form.error.notFinite': 'Число слишком велико.',
  'form.error.notWhole': 'Значение должно быть целым числом.',
  'notFound.type': 'Тип расчёта не найден',
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
  'form.title': 'Calculation inputs',
  'form.unit': 'Unit',
  'form.submit': 'Calculate',
  'form.submitting': 'Calculating…',
  'form.rejected': 'The request was rejected',
  'form.error.empty': 'Enter a value.',
  'form.error.notNumber': 'Enter a number.',
  'form.error.notFinite': 'The number is too large.',
  'form.error.notWhole': 'The value must be a whole number.',
  'notFound.type': 'Calculation type not found',
}

export interface Dictionaries {
  readonly ru: Dictionary
  readonly en: PartialDictionary
}

export const dictionaries: Dictionaries = { ru, en }
