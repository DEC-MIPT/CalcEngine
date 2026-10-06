import { useI18n } from '@/i18n/context'
import { languages } from '@/i18n/dictionary'

export function LanguageSwitch() {
  const { language, setLanguage, t } = useI18n()
  return (
    <div role="group" aria-label={t('language.switch')}>
      {languages.map((code) => (
        <button
          key={code}
          type="button"
          lang={code}
          aria-pressed={language === code}
          onClick={() => setLanguage(code)}
        >
          {t(code === 'ru' ? 'language.ru' : 'language.en')}
        </button>
      ))}
    </div>
  )
}
