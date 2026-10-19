import { useLayoutEffect, useMemo, useRef } from 'react'
import { typeset } from './typeset'

type FormulaProps = {
  latex: string
  display?: boolean
}

export function Formula({ latex, display = false }: FormulaProps) {
  const container = useRef<HTMLSpanElement>(null)
  const rendered = useMemo(() => typeset(latex, display), [latex, display])

  useLayoutEffect(() => {
    if (rendered) container.current?.replaceChildren(rendered)
  }, [rendered])

  if (!rendered) {
    return <code data-fallback="true">{latex}</code>
  }
  return <span ref={container} role="img" aria-label={latex} />
}
