export const PLAYBACK_CAP_MS = 10_000
export const STEP_MAX_MS = 600

const played = new Set<string>()

export function stepInterval(count: number): number {
  if (count <= 0) return 0
  return Math.min(STEP_MAX_MS, Math.floor(PLAYBACK_CAP_MS / count))
}

export function hasPlayed(resultId: string): boolean {
  return played.has(resultId)
}

export function markPlayed(resultId: string): void {
  played.add(resultId)
}

export function resetPlayed(): void {
  played.clear()
}
