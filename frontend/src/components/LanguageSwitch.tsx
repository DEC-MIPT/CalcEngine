import { useI18n } from '@/i18n/context'
import { languages } from '@/i18n/dictionary'

export function LanguageSwitch() {
  const { language, setLanguage, t } = useI18n()
  return (
    <div role="group" aria-label={t('language.switch')} className="inline-flex border border-input">
      {languages.map((code) => (
        <button
          key={code}
          type="button"
          lang={code}
          aria-pressed={language === code}
          onClick={() => setLanguage(code)}
          className="min-h-9 cursor-pointer px-3 text-sm transition-colors not-last:border-r not-last:border-input hover:bg-secondary aria-pressed:bg-primary aria-pressed:text-primary-foreground aria-pressed:hover:bg-primary"
        >
          {t(code === 'ru' ? 'language.ru' : 'language.en')}
        </button>
      ))}
    </div>
  )
}
