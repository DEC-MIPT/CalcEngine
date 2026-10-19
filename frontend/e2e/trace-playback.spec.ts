import { expect, test, type Page } from '@playwright/test'

const PASS_ID = '11111111-1111-4111-8111-111111111111'
const FAIL_ID = '22222222-2222-4222-8222-222222222222'
const STEPS = 9

test.skip(({ browserName }) => browserName !== 'chromium', 'the playback is recorded in Chromium')

test.use({
  reducedMotion: 'no-preference',
  viewport: { width: 1280, height: 900 },
  video: { mode: 'on', size: { width: 1280, height: 900 } },
})

async function openResult(page: Page, id: string) {
  await page.goto(`/calculations/${id}`)
  await expect(page.locator('[data-verdict]')).toBeVisible()
}

const steps = (page: Page) => page.locator('[data-step]')
const pending = (page: Page) => page.locator('[data-step][data-arrival="pending"]')
const stamp = (page: Page) => page.locator('[data-verdict]')

test.describe('recorded playback', () => {
  test('a passed check plays the steps one by one and stamps the verdict', async ({ page }, info) => {
    await openResult(page, PASS_ID)

    await expect(stamp(page)).toHaveAttribute('data-reveal', 'pending')
    await expect(page.locator('[data-skip-hint]')).toBeVisible()
    await page.screenshot({ path: info.outputPath('pass-1-start.png') })
    await expect(pending(page)).toHaveCount(STEPS - 4, { timeout: 4000 })
    await page.screenshot({ path: info.outputPath('pass-2-middle.png') })

    await expect(stamp(page)).toHaveAttribute('data-reveal', 'celebrate', { timeout: 10_000 })
    await expect(pending(page)).toHaveCount(0)
    await page.waitForTimeout(820)
    await page.screenshot({ path: info.outputPath('pass-3-stamp.png') })
    await page.waitForTimeout(1500)
    await page.screenshot({ path: info.outputPath('pass-4-end.png') })
  })

  test('a failed check plays the steps and shows the verdict at once', async ({ page }, info) => {
    await openResult(page, FAIL_ID)

    await expect(stamp(page)).toHaveAttribute('data-reveal', 'pending')
    await expect(stamp(page)).toHaveAttribute('data-reveal', 'plain', { timeout: 10_000 })
    await page.screenshot({ path: info.outputPath('fail-1-verdict.png') })
    await expect(stamp(page)).toHaveAttribute('aria-live', 'assertive')
    await page.waitForTimeout(1000)
  })
})

test('the whole playback of a 9-step trace stays under the cap', async ({ page }) => {
  await openResult(page, PASS_ID)
  const started = Date.now()

  await expect(pending(page)).toHaveCount(0, { timeout: 10_000 })

  expect(Date.now() - started).toBeLessThan(10_000)
})

test('reduced motion shows every step and the verdict at once', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await openResult(page, PASS_ID)

  await expect(steps(page)).toHaveCount(STEPS)
  await expect(pending(page)).toHaveCount(0)
  await expect(stamp(page)).toHaveAttribute('data-reveal', 'none')
  await expect(page.locator('[data-skip-hint]')).toHaveCount(0)
})

test('the same result opened again in the session does not play', async ({ page }) => {
  await openResult(page, PASS_ID)
  await expect(stamp(page)).toHaveAttribute('data-reveal', 'pending')
  await page.keyboard.press('Escape')
  await page.getByRole('link', { name: 'Запросить отчёт' }).first().click()
  await expect(page).toHaveURL(new RegExp(`/calculations/${PASS_ID}/report$`))

  await page.goBack()

  await expect(stamp(page)).toHaveAttribute('data-reveal', 'none')
  await expect(pending(page)).toHaveCount(0)
})

test('a click on the trace shows every remaining step at once', async ({ page }) => {
  await openResult(page, PASS_ID)
  await expect(pending(page)).not.toHaveCount(0)

  await page.locator('#trace-title').click()

  await expect(pending(page)).toHaveCount(0)
  await expect(stamp(page)).toHaveAttribute('data-reveal', 'none')
})

test('the space key shows every remaining step at once without scrolling', async ({ page }) => {
  await openResult(page, PASS_ID)
  await expect(pending(page)).not.toHaveCount(0)
  const scroll = await page.evaluate(() => window.scrollY)

  await page.keyboard.press('Space')

  await expect(pending(page)).toHaveCount(0)
  expect(await page.evaluate(() => window.scrollY)).toBe(scroll)
})

test('Tab during the playback never lands on a step that is not shown', async ({ page }) => {
  await openResult(page, PASS_ID)
  await expect(pending(page)).not.toHaveCount(0)

  await page.keyboard.press('Tab')

  await expect(pending(page)).toHaveCount(0)
  const focused = await page.evaluate(() => document.activeElement?.closest('[data-step][data-arrival="pending"]') !== null)
  expect(focused).toBe(false)
})
