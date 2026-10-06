import { expect, test } from '@playwright/test'

test('every step of a mocked result shows its formula typeset', async ({ page }) => {
  const problems: string[] = []
  page.on('pageerror', (error) => problems.push(error.message))

  await page.goto('/e2e/harness/formulas.html')

  const steps = page.locator('[data-step]')
  await expect(steps.first()).toBeVisible()
  const count = await steps.count()
  expect(count).toBeGreaterThan(0)
  for (let index = 0; index < count; index++) {
    const step = steps.nth(index)
    await expect(step.locator('[role="img"] svg')).toHaveCount(1)
    await expect(step.locator('[data-fallback]')).toHaveCount(0)
    const box = await step.locator('svg').boundingBox()
    expect(box?.width ?? 0).toBeGreaterThan(0)
  }
  expect(problems).toEqual([])
})
