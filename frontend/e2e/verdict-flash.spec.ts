import { expect, test } from '@playwright/test'

const PASS_ID = '11111111-1111-4111-8111-111111111111'

test.use({ reducedMotion: 'no-preference' })

test('nothing animates the verdict into view while the trace is still playing', async ({ page }) => {
  await page.addInitScript(() => {
    const seen = { frames: 0, showing: [] as string[] }
    ;(window as unknown as { __stampSeen: typeof seen }).__stampSeen = seen
    const sample = () => {
      const stamp = document.querySelector('[data-verdict]')
      if (stamp?.getAttribute('data-reveal') === 'pending') {
        seen.frames += 1
        for (const child of stamp.querySelectorAll(':scope > :not(.stamp-status)')) {
          for (const animation of child.getAnimations()) {
            const effect = animation.effect as KeyframeEffect
            if (effect.getKeyframes().some((frame) => Number(frame.opacity ?? 0) > 0)) {
              seen.showing.push((animation as CSSAnimation).animationName)
            }
          }
        }
      }
      requestAnimationFrame(sample)
    }
    requestAnimationFrame(sample)
  })
  await page.goto(`/calculations/${PASS_ID}`)
  await expect(page.locator('[data-verdict]')).toHaveAttribute('data-reveal', 'pending')
  await page.waitForTimeout(600)

  const seen = await page.evaluate(() => (window as unknown as { __stampSeen: { frames: number; showing: string[] } }).__stampSeen)

  expect(seen.frames).toBeGreaterThan(10)
  expect([...new Set(seen.showing)]).toEqual([])
})

test('a skipped playback shows the verdict at once, with no fade', async ({ page }) => {
  await page.goto(`/calculations/${PASS_ID}`)
  await expect(page.locator('[data-verdict]')).toHaveAttribute('data-reveal', 'pending')

  await expect(async () => {
    await page.keyboard.press('Escape')
    await expect(page.locator('[data-verdict]')).toHaveAttribute('data-reveal', 'none', { timeout: 500 })
  }).toPass({ timeout: 5000 })

  const state = await page.locator('[data-verdict]').evaluate((stamp) =>
    [...stamp.children].map((child) => ({ animations: child.getAnimations().length, opacity: getComputedStyle(child).opacity })),
  )
  expect(state.every(({ animations, opacity }) => animations === 0 && opacity === '1')).toBe(true)
})
