import { useEffect, useMemo, useState, type ReactNode } from 'react'
import { I18nContext, type I18n } from './context'
import { dictionaries, type Language } from './dictionary'
import { formatNumber, translate } from './translate'

export function I18nProvider({
  children,
  initialLanguage = 'ru',
}: {
  children: ReactNode
  initialLanguage?: Language
}) {
  const [language, setLanguage] = useState<Language>(initialLanguage)

  useEffect(() => {
    document.documentElement.lang = language
  }, [language])

  const value = useMemo<I18n>(
    () => ({
      language,
      setLanguage,
      t: (key) => translate(dictionaries, language, key),
      formatNumber: (number) => formatNumber(number, language),
    }),
    [language],
  )

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}
