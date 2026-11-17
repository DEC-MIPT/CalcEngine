import { useId } from 'react'
import { useI18n } from '@/i18n/context'

export function LoadsDirections() {
  const { t } = useI18n()
  const id = useId()
  const heading = `${id}-heading`
  const title = `${id}-title`
  const description = `${id}-description`
  return (
    <section aria-labelledby={heading} className="grid gap-4 border-y border-border py-5">
      <h2 id={heading} className="text-xl">{t('loads.directions.title')}</h2>
      <div className="grid min-w-0 gap-5 md:grid-cols-[minmax(0,22rem)_minmax(0,1fr)] md:gap-8">
        <figure className="grid min-w-0 content-start gap-3">
          <svg
            role="img"
            aria-labelledby={`${title} ${description}`}
            viewBox="0 0 360 290"
            className="mx-auto block w-full max-w-[22rem] text-foreground"
          >
            <title id={title}>{t('loads.directions.plan')}</title>
            <desc id={description}>{t('loads.directions.axes')}</desc>
            <g fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="85" y="55" width="170" height="170" />
              <path d="M55 140H315M170 255V15" strokeDasharray="4 4" />
              <path d="m306 135 9 5-9 5M165 24l5-9 5 9" />
              <path d="M85 245v18m170-18v18M85 254h170M65 55H47m18 170H47M56 55v170" />
              <path d="m92 250-7 4 7 4m156-8 7 4-7 4M52 62l4-7 4 7m-8 156 4 7 4-7" />
            </g>
            <g fill="currentColor" className="font-mono text-sm">
              <text x="318" y="145">+x</text>
              <text x="182" y="23">+y</text>
              <text x="28" y="145">−x</text>
              <text x="178" y="235">−y</text>
              <text x="170" y="281" textAnchor="middle">b · x</text>
              <text x="20" y="93">l · y</text>
              <text x="263" y="48">pp (+,+)</text>
              <text x="263" y="221">pm (+,−)</text>
              <text x="77" y="48" textAnchor="end">mp (−,+)</text>
              <text x="77" y="221" textAnchor="end">mm (−,−)</text>
            </g>
            <circle cx="170" cy="140" r="3" fill="currentColor" />
          </svg>
          <figcaption className="grid gap-2 text-sm">
            <p>{t('loads.directions.axes')}</p>
            <p>{t('loads.directions.corners')}</p>
          </figcaption>
        </figure>
        <div className="grid min-w-0 content-start gap-4 text-sm">
          <div className="grid gap-2">
            <h3 className="font-semibold">{t('loads.directions.signs')}</h3>
            <p>{t('loads.directions.variation')}</p>
            <p className="font-mono">Mx_base = Mx + Qx·h<br />My_base = My + Qy·h</p>
            <p>{t('loads.directions.transfer')}</p>
          </div>
          <dl className="grid grid-cols-[auto_minmax(0,1fr)] gap-x-3 gap-y-2">
            <dt className="font-mono">N</dt><dd>{t('loads.directions.weight')}</dd>
            <dt className="font-mono">d</dt><dd>{t('loads.directions.d')}</dd>
            <dt className="font-mono">h</dt><dd>{t('loads.directions.h')}</dd>
            <dt className="font-mono">d_1</dt><dd>{t('loads.directions.d1')}</dd>
            <dt className="font-mono">d_b</dt><dd>{t('loads.directions.db')}</dd>
          </dl>
        </div>
      </div>
      <div className="grid gap-2 text-sm md:grid-cols-2 md:gap-8">
        <p>{t('loads.directions.geometry')}</p>
        <p>{t('loads.directions.angle')}</p>
      </div>
    </section>
  )
}
