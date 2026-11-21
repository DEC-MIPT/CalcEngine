import { expect, test } from '@playwright/test'
import { loadsCentralEnvelope, loadsContactRefusalEnvelope, passEnvelope } from '../src/mocks/fixtures'

for (const width of [1280, 320]) {
  test.describe(`compact trace at ${width}px`, () => {
    test.use({ reducedMotion: 'reduce', viewport: { width, height: 900 } })

    for (const envelope of [loadsCentralEnvelope, loadsContactRefusalEnvelope]) {
      test(`preserves and reveals the complete ${envelope.verdict} trace`, async ({ page }) => {
        await page.goto(`/calculations/${envelope.result_id}`)
        const list = page.locator('[data-trace-layout="compact"]')
        const rows = list.locator(':scope > [data-step]')
        await expect(rows).toHaveCount(envelope.trace.length)
        expect(await rows.evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-step')))).toEqual(envelope.trace.map((step) => step.step_id))
        await expect(list.locator('[data-step-heading] > button[aria-expanded="false"]')).toHaveCount(envelope.trace.length)
        expect(await list.locator('[data-trace-section]').count()).toBe(envelope.verdict === 'refused' ? 7 : 8)
        await expect(list.locator('[inert], [data-arrival="pending"]')).toHaveCount(0)
        const compactHeight = await list.evaluate((node) => node.getBoundingClientRect().height)
        if (envelope.verdict === 'refused') await expect(page.locator('[data-output], [data-verdict], [data-check-step]')).toHaveCount(0)

        const firstButton = rows.first().locator('[data-step-heading] > button')
        await firstButton.focus()
        await page.keyboard.press('Enter')
        await expect(firstButton).toHaveAttribute('aria-expanded', 'true')
        await expect(rows.first().locator('.step-details')).toBeVisible()
        await page.keyboard.press('Space')
        await expect(firstButton).toHaveAttribute('aria-expanded', 'false')
        await page.getByRole('button', { name: 'Развернуть все шаги', exact: true }).click()
        await expect(list.locator('[data-step-heading] > button[aria-expanded="true"]')).toHaveCount(envelope.trace.length)
        expect(await list.evaluate((node) => node.getBoundingClientRect().height)).toBeGreaterThan(compactHeight * 2)
        for (let index = 0; index < envelope.trace.length; index++) {
          await expect(rows.nth(index)).toHaveAttribute('id', `trace-step-${index}`)
          await expect(rows.nth(index).locator('.step-details [role="region"]').first().getByRole('img')).toHaveAttribute('aria-label', envelope.trace[index].expression)
        }
        await page.getByRole('button', { name: 'Свернуть все шаги', exact: true }).click()
        await expect(list.locator('[data-step-heading] > button[aria-expanded="false"]')).toHaveCount(envelope.trace.length)
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
      })
    }

    test('keeps the historical pilot initially expanded', async ({ page }) => {
      await page.goto(`/calculations/${passEnvelope.result_id}`)
      const list = page.locator('[data-trace-layout="expanded"]')
      await expect(list.locator('[data-step]')).toHaveCount(passEnvelope.trace.length)
      await expect(list.locator('[data-step-heading] > button[aria-expanded="true"]')).toHaveCount(passEnvelope.trace.length)
      await expect(list.locator('[data-trace-section]')).toHaveCount(0)
    })
  })
}
