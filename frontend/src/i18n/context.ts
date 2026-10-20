import { createContext, useContext } from 'react'
import type { Language, TextKey } from './dictionary'

export interface I18n {
  language: Language
  setLanguage: (language: Language) => void
  t: (key: TextKey) => string
  formatNumber: (value: number, minimumFractionDigits?: number) => string
}

export const I18nContext = createContext<I18n | null>(null)

export function useI18n(): I18n {
  const value = useContext(I18nContext)
  if (value === null) {
    throw new Error('useI18n must be used inside I18nProvider')
  }
  return value
}
