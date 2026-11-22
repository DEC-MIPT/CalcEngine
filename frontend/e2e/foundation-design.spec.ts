import { expect, test, type Page } from '@playwright/test'
import type { components } from '../src/api/schema'
import { selectionSelected, weightsCentralRequest, weightsContactRefusalEnvelope } from '../src/mocks/designFixtures'

const form = '/calculations/new?type=foundations_shallow_loads'
const weights = '/calculations/new?type=foundations_shallow_weights'
test.use({ reducedMotion: 'reduce', viewport: { width: 320, height: 740 } })

async function fill(page: Page, inputs: components['schemas']['CalculationRequest']['inputs']) {
  for (const [name, quantity] of Object.entries(inputs)) {
    const field = page.locator(`#field-${name}`)
    const unit = field.locator('..').locator('select')
    if (await unit.count()) await unit.selectOption(quantity.unit)
    await field.fill(String(quantity.value))
  }
}

async function noPageOverflow(page: Page) {
  const overflow = await page.evaluate(() => Array.from(document.querySelectorAll('main *'))
    .filter((node) => node.getBoundingClientRect().right > 320 && getComputedStyle(node).position !== 'absolute')
    .slice(0, 8).map((node) => node.outerHTML.split('>')[0]))
  expect(await page.evaluate(() => document.documentElement.scrollWidth), overflow.join('\n')).toBeLessThanOrEqual(320)
}

async function report(page: Page, filename: string) {
  await page.getByRole('link', { name: 'Запросить отчёт' }).click()
  await page.getByLabel('Обозначение документа').fill('DEC-FOUNDATION')
  await page.getByLabel('Наименование документа').fill('Проектирование фундамента')
  await page.getByLabel('Организация').fill('DEC')
  await page.getByRole('switch', { name: 'Заполнить блок подписей' }).click()
  await page.getByRole('button', { name: 'Сформировать отчёт' }).click()
  const download = page.waitForEvent('download')
  await page.getByRole('button', { name: `Скачать ${filename}`, exact: true }).click()
  expect((await download).suggestedFilename()).toBe(filename)
}

test('check explicit weights, inspect stored diagrams and download an ordinary report', async ({ page }) => {
  await page.goto(weights)
  await page.locator('#field-G_fund').waitFor()
  await fill(page, weightsCentralRequest.inputs)
  await expect(page.getByRole('link', { name: 'Подобрать размеры' })).toHaveCount(0)
  await noPageOverflow(page)
  await page.getByRole('button', { name: 'Рассчитать' }).press('Enter')
  await expect(page.getByRole('heading', { name: 'Эпюра давлений' })).toBeVisible()
  await expect(page.getByRole('table', { name: 'Давления в углах' }).getByRole('row')).toHaveCount(5)
  await expect(page.locator('[data-step="G_sum"] button')).toHaveAttribute('aria-expanded', 'true')
  await noPageOverflow(page)
  await report(page, 'report.docx')
})

test('search ordered candidates, reload the stored comparison and download its report', async ({ page }) => {
  await page.goto(form)
  await page.getByRole('link', { name: 'Подобрать размеры' }).press('Enter')
  await page.locator('#candidate-0-b').waitFor()
  await fill(page, selectionSelected.request.common_inputs)
  for (const [index, { b, l }] of selectionSelected.request.candidates.entries()) {
    if (index > 0) await page.getByRole('button', { name: 'Добавить вариант' }).press('Enter')
    await page.locator(`#candidate-${index}-b`).fill(String(b.value))
    await page.locator(`#candidate-${index}-l`).fill(String(l.value))
  }
  await noPageOverflow(page)
  await page.getByRole('button', { name: 'Подобрать размеры' }).press('Enter')
  await expect(page.getByRole('link', { name: 'Открыть выбранный расчёт' })).toHaveAttribute('href', `/calculations/${selectionSelected.selected_result_id}`)
  await page.reload()
  const evidence = page.locator('[data-candidate="1"] summary')
  await evidence.press('Enter')
  await expect(page.locator('[data-candidate="1"] [data-check-step]')).toHaveCount(4)
  await noPageOverflow(page)
  await report(page, 'foundation-selection-report.docx')
})

test('refused contact shows signed diagnostic pressure without passing checks', async ({ page }) => {
  await page.goto(`/calculations/${weightsContactRefusalEnvelope.result_id}`)
  await expect(page.getByText(/Диагностические давления без перераспределения/)).toBeVisible()
  const table = page.getByRole('table', { name: 'Давления в углах' })
  await expect(table).toContainText(/[-−]\d/)
  await expect(page.locator('[data-check-step]')).toHaveCount(0)
  await noPageOverflow(page)
})


test('keyboard focus recovers after deleting a candidate and after an API field error', async ({ page }) => {
  await page.addInitScript(() => {
    const original = window.fetch.bind(window)
    window.fetch = (input, init) => {
      if (input instanceof Request && input.method === 'POST' && new URL(input.url).pathname === '/foundation-selections') {
        return Promise.resolve(Response.json({ code: 'invalid_input', message: 'Invalid', fields: [
          { location: ['body', 'candidates', 0, 'l'], message: 'Проверьте длину.' },
        ] }, { status: 422 }))
      }
      return original(input, init)
    }
  })
  await page.goto(`${form}&task=selection`)
  await page.getByRole('button', { name: 'Добавить вариант' }).press('Enter')
  await page.getByRole('button', { name: 'Удалить вариант 2' }).press('Enter')
  await expect(page.locator('#candidate-0-b')).toBeFocused()
  await fill(page, selectionSelected.request.common_inputs)
  await page.locator('#candidate-0-b').fill('2')
  await page.locator('#candidate-0-l').fill('3')
  await page.getByRole('button', { name: 'Подобрать размеры' }).press('Enter')
  await expect(page.getByText('Проверьте длину.')).toBeVisible()
  await expect(page.locator('#candidate-0-l')).toBeFocused()
})
