import { afterEach, describe, expect, it } from 'vitest'
import { hasPlayed, markPlayed, PLAYBACK_CAP_MS, resetPlayed, STEP_MAX_MS, stepInterval } from './playback'

afterEach(() => resetPlayed())

describe('stepInterval (trace playback)', () => {
  it.each([1, 3, 9, 15, 17, 50, 1000])('keeps %i steps under the cap and each step under the maximum', (count) => {
    const interval = stepInterval(count)

    expect(interval).toBeGreaterThan(0)
    expect(interval).toBeLessThanOrEqual(STEP_MAX_MS)
    expect(interval * count).toBeLessThanOrEqual(PLAYBACK_CAP_MS)
  })

  it('shortens the interval rather than lengthening the playback', () => {
    expect(stepInterval(9)).toBe(STEP_MAX_MS)
    expect(stepInterval(50)).toBe(200)
    expect(stepInterval(50)).toBeLessThan(stepInterval(15))
  })

  it('has no interval without steps', () => {
    expect(stepInterval(0)).toBe(0)
  })
})

describe('played results (trace playback)', () => {
  it('remembers a result once it is marked and forgets it on reset', () => {
    expect(hasPlayed('a')).toBe(false)

    markPlayed('a')

    expect(hasPlayed('a')).toBe(true)
    expect(hasPlayed('b')).toBe(false)
    resetPlayed()
    expect(hasPlayed('a')).toBe(false)
  })
})
