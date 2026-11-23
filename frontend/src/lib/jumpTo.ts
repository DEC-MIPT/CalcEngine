import type { MouseEvent } from 'react'

export function focusAnchor(id: string): boolean {
  const target = document.getElementById(id)
  if (!target) return false
  target.scrollIntoView({ block: 'start' })
  target.focus({ preventScroll: true })
  return true
}

export function traceStepAnchor(hash: string, stepCount: number): string | undefined {
  const match = /^#trace-step-(0|[1-9]\d*)$/.exec(hash)
  return match && Number(match[1]) < stepCount ? hash.slice(1) : undefined
}

export function jumpTo(event: MouseEvent<HTMLAnchorElement>, id: string): boolean {
  if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return false
  if (!focusAnchor(id)) return false
  event.preventDefault()
  return true
}
