export function prefersReducedMotion(): boolean {
  if (typeof window.matchMedia !== 'function') return true
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export function withMinimumDuration<T>(work: Promise<T>, milliseconds: number): Promise<T> {
  if (milliseconds <= 0) return work
  const pause = new Promise<void>((resolve) => setTimeout(resolve, milliseconds))
  return Promise.all([work, pause]).then(([value]) => value)
}
