import { expect, test } from '@playwright/test'

const PASS_ID = '11111111-1111-4111-8111-111111111111'

test.use({ reducedMotion: 'reduce', viewport: { width: 1280, height: 900 } })

test('the steps link of the stamp brings the trace heading to the top and focuses it', async ({ page }) => {
  await page.goto(`/calculations/${PASS_ID}`)
  const heading = page.locator('#trace-title')
  await expect(heading).toBeVisible()
  const historyLength = await page.evaluate(() => history.length)

  await page.locator('[data-to-trace]').click()

  await expect(heading).toBeFocused()
  const top = await heading.evaluate((element) => element.getBoundingClientRect().top)
  expect(top).toBeGreaterThanOrEqual(0)
  expect(top).toBeLessThan(40)
  expect(page.url()).not.toContain('#')
  expect(await page.evaluate(() => history.length)).toBe(historyLength)
})

test('the steps link works from the keyboard', async ({ page }) => {
  await page.goto(`/calculations/${PASS_ID}`)
  await expect(page.locator('[data-verdict]')).toBeFocused()

  await page.locator('[data-to-trace]').focus()
  await page.keyboard.press('Enter')

  await expect(page.locator('#trace-title')).toBeFocused()
})

test('a tick of the trace ruler brings its step to the top', async ({ page }) => {
  await page.goto(`/calculations/${PASS_ID}`)
  await expect(page.locator('[data-ruler-verdict]')).toBeVisible()
  const historyLength = await page.evaluate(() => history.length)

  await page.locator('[data-tick="5"]').click()

  const step = page.locator('#trace-step-5')
  await expect(step).toBeInViewport()
  const top = await step.evaluate((element) => element.getBoundingClientRect().top)
  expect(top).toBeGreaterThanOrEqual(0)
  expect(top).toBeLessThan(40)
  expect(page.url()).not.toContain('#')
  expect(await page.evaluate(() => history.length)).toBe(historyLength)
})
