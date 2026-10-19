import type { MouseEvent } from 'react'

export function jumpTo(event: MouseEvent<HTMLAnchorElement>, id: string): void {
  if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return
  const target = document.getElementById(id)
  if (!target) return
  event.preventDefault()
  target.scrollIntoView({ block: 'start' })
  target.focus({ preventScroll: true })
}
