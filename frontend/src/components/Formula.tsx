import { useLayoutEffect, useMemo, useRef } from 'react'
import { typeset } from './typeset'

type FormulaProps = {
  latex: string
  display?: boolean
  presentation?: string | null
}

export function Formula({ latex, display = false, presentation }: FormulaProps) {
  const container = useRef<HTMLSpanElement>(null)
  const rendered = useMemo(() => presentation === null ? null : typeset(presentation ?? latex, display), [latex, display, presentation])

  useLayoutEffect(() => {
    if (rendered) container.current?.replaceChildren(rendered)
  }, [rendered])

  if (!rendered) {
    return <code data-fallback="true" data-source-expression={latex}>{latex}</code>
  }
  return <span ref={container} role="img" aria-label={latex} data-source-expression={latex} />
}
