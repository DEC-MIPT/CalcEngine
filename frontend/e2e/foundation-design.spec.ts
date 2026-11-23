import { expect, test, type Page } from '@playwright/test'
import type { components } from '../src/api/schema'
import { selectionSelected, weightsCentralEnvelope, weightsCentralRequest, weightsContactRefusalEnvelope } from '../src/mocks/designFixtures'

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

test('opens the editable synthetic example and submits it through the ordinary calculation API', async ({ page }) => {
  await page.goto('/')
  const ordinary = page.getByRole('link', { name: 'Расчет фундамента мелкого заложения (демо)', exact: true })
  const example = page.getByRole('link', { name: /демо.*с примером/ })
  await ordinary.press('Enter')
  const b = page.locator('#field-b')
  await expect(b).toHaveValue('')
  await b.fill('1.75')
  await page.goBack()

  const submissions: unknown[] = []
  page.on('request', (request) => {
    if (request.method() === 'POST' && new URL(request.url()).pathname === '/calculations') submissions.push(request.postDataJSON())
  })
  await example.press('Enter')
  await expect(page.getByText(/Предзаполнены редактируемые синтетические данные/)).toContainText('weights-C')
  for (const [name, { value, unit }] of Object.entries(weightsCentralRequest.inputs)) {
    const field = page.locator(`#field-${name}`)
    await expect(field).toHaveValue(String(value))
    const units = field.locator('..').locator('select')
    if (await units.count()) await expect(units).toHaveValue(unit)
  }
  expect(submissions).toHaveLength(0)
  await noPageOverflow(page)
  await page.getByRole('button', { name: 'Рассчитать' }).press('Enter')
  await expect(page.getByRole('heading', { name: 'Эпюра давлений' })).toBeVisible()
  expect(submissions).toEqual([weightsCentralRequest])
  await page.getByRole('link', { name: 'Изменить исходные данные' }).press('Enter')
  await expect(page).toHaveURL(/example=weights-C/)
  await expect(b).toHaveValue('2')
  await b.fill('2.25')
  const registry = page.getByRole('link', { name: 'Типы расчётов', exact: true })
  await registry.press('Enter')
  await ordinary.press('Enter')
  await expect(b).toHaveValue('1.75')
  await registry.press('Enter')
  await example.press('Enter')
  await expect(b).toHaveValue('2.25')
})

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
  const index = weightsCentralEnvelope.trace.findIndex(({ step_id }) => step_id === 'G_sum')
  const tick = page.locator(`[data-tick="${index}"]`)
  await expect(page.locator('[data-tick]')).toHaveCount(weightsCentralEnvelope.trace.length)
  await expect(tick).toHaveAccessibleName(`${index + 1}. G_sum`)
  expect((await tick.boundingBox())?.width).toBeGreaterThanOrEqual(24)
  await tick.press('Enter')
  const step = page.locator('[data-step="G_sum"]')
  await expect(step).toBeFocused()
  await expect(step.getByText('СП 22.13330.2016', { exact: true })).toHaveCount(1)
  await expect(step).toContainText('таблица 5.4')
  await expect(step).toContainText('формула (5.7)')
  await expect(page.locator('[data-step="gamma_c1"] [data-summary]')).toHaveText('1,10')
  for (const cell of await page.getByRole('table', { name: 'Давления в углах' }).getByRole('cell').all()) {
    await expect(cell).toHaveText(/^[-−]?\d+,\d{2} /)
  }
  await noPageOverflow(page)
  await report(page, 'report.docx')
})

test('clicking a pending demo ruler tick finishes playback and opens that step', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'no-preference' })
  await page.setViewportSize({ width: 1280, height: 900 })
  await page.goto(`/calculations/${weightsCentralEnvelope.result_id}`)
  const index = weightsCentralEnvelope.trace.length - 1
  const tick = page.locator(`[data-tick="${index}"]`)
  await expect(page.locator('[data-ruler-cursor]')).toBeVisible()
  await expect(tick).toHaveAttribute('data-arrival', 'pending')
  await tick.click()
  await expect(page.locator(`#trace-step-${index}`)).toBeFocused()
  await expect(page.locator('[data-ruler-verdict="pass"]')).toBeVisible()
  await expect(page.locator('[data-ruler-cursor]')).toHaveCount(0)
})

for (const { mode, route, fields, title } of [
  { mode: 'explicit weights', route: weights, fields: 19, title: 'Расчет фундамента мелкого заложения (демо)' },
  { mode: 'averaged weights', route: form, fields: 15, title: 'Усреднённые веса' },
  { mode: 'size selection', route: `${form}&task=selection`, fields: 13, title: 'Подобрать размеры' },
]) {
  test(`${mode} centers the diagram and keeps symbols clear of labels`, async ({ page }) => {
    await page.goto(route)
    await expect(page.locator('p').and(page.getByText(title, { exact: true }))).toBeVisible()
    const guidance = page.getByRole('region', { name: 'Схема направлений и знаков' })
    const diagram = guidance.getByRole('img', { name: /Прямоугольная подошва: вид сверху/ })
    await expect(diagram).toBeVisible()
    const caption = guidance.locator('figcaption')
    await expect(caption).toContainText('Углы обозначены знаками координат')
    await expect(caption).toHaveCSS('position', 'absolute')
    await expect(caption).toHaveCSS('width', '1px')
    const symbols = page.locator('[data-row] > span:first-child mjx-container svg')
    await expect(symbols).toHaveCount(fields)
    await page.evaluate(() => document.fonts.ready)

    for (const width of [320, 640, 768, 1280]) {
      await page.setViewportSize({ width, height: 740 })
      const centerOffset = await diagram.evaluate((svg) => {
        const section = svg.closest('section')!.getBoundingClientRect()
        const rect = svg.getBoundingClientRect()
        return Math.abs((rect.left + rect.width / 2) - (section.left + section.width / 2))
      })
      expect(centerOffset, `diagram center offset at ${width}px`).toBeLessThanOrEqual(1)
      const overlappingFields = await symbols.evaluateAll((items) => items.flatMap((symbol) => {
        const label = symbol.closest('[data-row]')?.querySelector('label')
        return label && symbol.getBoundingClientRect().right <= label.getBoundingClientRect().left ? [] : [label?.htmlFor]
      }))
      expect(overlappingFields, `symbol overlap at ${width}px`).toEqual([])
      expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(width)
    }
  })
}

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
  await page.emulateMedia({ reducedMotion: 'no-preference' })
  await page.goto(`/calculations/${weightsContactRefusalEnvelope.result_id}`)
  await expect(page.getByText(/Диагностические давления без перераспределения/)).toBeVisible()
  const table = page.getByRole('table', { name: 'Давления в углах' })
  await expect(table).toContainText(/[-−]\d/)
  await expect(page.locator('[data-check-step]')).toHaveCount(0)
  await expect(page.locator('[data-tick]')).toHaveCount(weightsContactRefusalEnvelope.trace.length)
  await expect(page.locator('[data-arrival="pending"]')).toHaveCount(0)
  const mark = page.locator('[data-ruler-verdict="refused"]')
  await expect(mark).toBeVisible()
  await expect(mark.locator('path')).toHaveAttribute('data-mark', 'refused')
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
