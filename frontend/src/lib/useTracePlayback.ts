import { useCallback, useEffect, useLayoutEffect, useState } from 'react'
import { flushSync } from 'react-dom'
import { prefersReducedMotion } from './motion'
import { hasPlayed, markPlayed, stepInterval } from './playback'

export type PlaybackPhase = 'idle' | 'playing' | 'ended' | 'skipped'

export interface TracePlayback {
  shown: number
  phase: PlaybackPhase
  skip: () => void
}

export type Arrival = 'pending' | 'reveal' | 'shown'

export function arrivalOf(index: number, playback: TracePlayback | undefined): Arrival {
  if (!playback) return 'shown'
  if (index >= playback.shown) return 'pending'
  return playback.phase === 'playing' || playback.phase === 'ended' ? 'reveal' : 'shown'
}

const SKIP_KEYS = new Set([' ', 'Enter', 'Escape'])
const CONTROLS = 'a, button, input, select, textarea, summary, [contenteditable]'

function isControl(target: EventTarget | null): boolean {
  return target instanceof Element && target.closest(CONTROLS) !== null
}

export function useTracePlayback(resultId: string, stepCount: number): TracePlayback {
  const [animated] = useState(() => stepCount > 0 && !hasPlayed(resultId) && !prefersReducedMotion())
  const [shown, setShown] = useState(animated ? 0 : stepCount)
  const [skipped, setSkipped] = useState(false)
  const playing = shown < stepCount

  useEffect(() => markPlayed(resultId), [resultId])

  const skip = useCallback(() => {
    setSkipped(true)
    setShown(stepCount)
  }, [stepCount])

  useEffect(() => {
    if (!playing) return
    const timer = setTimeout(() => setShown((count) => count + 1), stepInterval(stepCount))
    return () => clearTimeout(timer)
  }, [playing, shown, stepCount])

  useLayoutEffect(() => {
    if (!playing) return
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        flushSync(skip)
        return
      }
      if (!SKIP_KEYS.has(event.key)) return
      if (!isControl(event.target)) event.preventDefault()
      skip()
    }
    document.addEventListener('keydown', onKeyDown)
    document.addEventListener('click', skip)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      document.removeEventListener('click', skip)
    }
  }, [playing, skip])

  let phase: PlaybackPhase = 'idle'
  if (playing) phase = 'playing'
  else if (skipped) phase = 'skipped'
  else if (animated) phase = 'ended'
  return { shown, phase, skip }
}
