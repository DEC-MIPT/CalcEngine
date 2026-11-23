import { useId } from 'react'
import { useI18n } from '@/i18n/context'

export function LoadsDirections({ explicit = false }: { explicit?: boolean }) {
  const { t } = useI18n()
  const id = useId()
  const heading = `${id}-heading`
  const title = `${id}-title`
  const description = `${id}-description`
  return (
    <section aria-labelledby={heading} className="grid gap-4 border-y border-border py-5">
      <h2 id={heading} className="text-xl">{t('loads.directions.title')}</h2>
      <figure className="min-w-0">
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
        <figcaption className="sr-only">
          <p>{t('loads.directions.corners')}</p>
          <p>{t('loads.directions.variation')}</p>
          <p>Mx_base = Mx + Qx·h{explicit && ' + Mx_add_base'}<br />My_base = My + Qy·h{explicit && ' + My_add_base'}</p>
          <p>{t(explicit ? 'foundation.explicitHint' : 'loads.directions.transfer')}</p>
          <dl>
            {!explicit && <><dt>N</dt><dd>{t('loads.directions.weight')}</dd>
            <dt>d</dt><dd>{t('loads.directions.d')}</dd></>}
            <dt>h</dt><dd>{t('loads.directions.h')}</dd>
            <dt>d_1</dt><dd>{t('loads.directions.d1')}</dd>
            <dt>d_b</dt><dd>{t('loads.directions.db')}</dd>
          </dl>
          <p>{t('loads.directions.geometry')}</p>
          <p>{t('loads.directions.angle')}</p>
        </figcaption>
      </figure>
    </section>
  )
}
