import { expect, test, type Page } from '@playwright/test'
import { selectionSelected, weightsCentralRequest } from '../src/mocks/designFixtures'
import { LOADS_TYPE, loadsCentralEnvelope, loadsCentralInputs, loadsContactRefusalEnvelope, loadsContactRefusalInputs } from '../src/mocks/loadsFixtures'

const PASS_ID = '11111111-1111-4111-8111-111111111111'
const RUNS = 20
const LIMIT_MS = 1000
const INPUTS = { b: '2', d_1: '1.5', d_b: '0', gamma_II: '18', gamma_II_prime: '18', c_II: '10', phi_II: '20', p: '100' }
const REPORT = {
  'Обозначение документа': 'ДЕК-2026-001-РР',
  'Наименование документа': 'Расчёт сопротивления грунта',
  Организация: 'ООО «Проект»',
  'Разработал: Фамилия': 'Иванов',
  'Разработал: Дата': '2026-10-07',
  'Нормоконтроль: Фамилия': 'Петрова',
  'Нормоконтроль: Дата': '2026-10-08',
}

test.skip(({ browserName }) => browserName !== 'chromium', 'the transition time is measured in Chromium')
test.use({ viewport: { width: 1280, height: 900 } })
test.describe.configure({ timeout: 120_000 })

declare global {
  interface Window {
    __responses: { url: string; at: number }[]
    __rendered: Record<string, number>
    __watch: (name: string, selector: string) => void
  }
}

async function instrument(page: Page) {
  await page.addInitScript(() => {
    window.__responses = []
    window.__rendered = {}
    const original = window.fetch.bind(window)
    window.fetch = async (...args: Parameters<typeof fetch>) => {
      const response = await original(...args)
      const [input] = args
      const url = input instanceof Request ? input.url : String(input)
      window.__responses.push({ url, at: performance.now() })
      return response
    }
    window.__watch = (name, selector) => {
      const seen = () => {
        if (document.querySelector(selector) && !(name in window.__rendered)) {
          window.__rendered[name] = performance.now()
          observer.disconnect()
        }
      }
      const observer = new MutationObserver(seen)
      observer.observe(document, { childList: true, subtree: true, attributes: true })
      seen()
    }
  })
}

async function elapsed(page: Page, name: string, path: RegExp) {
  return page.evaluate(
    ({ name, source }) => {
      const pattern = new RegExp(source)
      const response = window.__responses.filter((entry) => pattern.test(new URL(entry.url).pathname)).at(-1)!
      return window.__rendered[name] - response.at
    },
    { name, source: path.source },
  )
}

function percentile95(samples: number[]) {
  const sorted = [...samples].sort((left, right) => left - right)
  return sorted[Math.ceil(sorted.length * 0.95) - 1]
}

async function measure(page: Page, run: (page: Page) => Promise<number>) {
  await instrument(page)
  const samples: number[] = []
  for (let index = 0; index < RUNS; index += 1) samples.push(await run(page))
  test.info().annotations.push({ type: 'p95 ms', description: percentile95(samples).toFixed(1) })
  return percentile95(samples)
}

test('type selection to the input form (8.9)', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto('/')
    await current.locator('a[href="/calculations/new?type=foundations_shallow_r"]').waitFor()
    await current.evaluate(() => window.__watch('form', '#field-b'))
    await current.locator('a[href="/calculations/new?type=foundations_shallow_r"]').click()
    await expect(current.locator('#field-b')).toBeVisible()
    return elapsed(current, 'form', /\/calculation-types$/)
  })
  expect(p95).toBeLessThan(LIMIT_MS)
})

test('the submitted form to the result, with the minimum computation trace (8.9)', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto('/calculations/new?type=foundations_shallow_r')
    for (const [name, value] of Object.entries(INPUTS)) await current.locator(`#field-${name}`).fill(value)
    await current.evaluate(() => window.__watch('result', '[data-verdict]'))
    await current.getByRole('button', { name: 'Рассчитать' }).click()
    await expect(current.locator('[data-verdict]')).toBeVisible()
    return elapsed(current, 'result', /\/calculations$/)
  })
  expect(p95).toBeLessThan(LIMIT_MS)
})

test('a result opened by its address (8.9)', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto('/nowhere')
    await current.evaluate(() => window.__watch('opened', '[data-verdict]'))
    await current.evaluate((id) => {
      history.pushState({}, '', `/calculations/${id}`)
      dispatchEvent(new PopStateEvent('popstate'))
    }, PASS_ID)
    await expect(current.locator('[data-verdict]')).toBeVisible()
    return elapsed(current, 'opened', /\/calculations\/[\w-]+$/)
  })
  expect(p95).toBeLessThan(LIMIT_MS)
})

test('the submitted report form to the issued stamp (8.9)', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto(`/calculations/${PASS_ID}/report`)
    for (const [label, value] of Object.entries(REPORT)) await current.getByLabel(label, { exact: true }).fill(value)
    await current.evaluate(() => window.__watch('stamp', '[data-report-stamp]'))
    await current.locator('form button[type="submit"]').click()
    await expect(current.locator('[data-report-stamp]')).toBeVisible()
    return elapsed(current, 'stamp', /\/report$/)
  })
  expect(p95).toBeLessThan(LIMIT_MS)
})

test('loads type selection to the fifteen-input form uses the same p95 policy', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto('/')
    const type = current.locator(`a[href="/calculations/new?type=${LOADS_TYPE}"]`)
    await type.waitFor()
    await current.evaluate(() => window.__watch('loads-form', '#field-Qy'))
    await type.click()
    await expect(current.locator('#field-Qy')).toBeVisible()
    return elapsed(current, 'loads-form', /\/calculation-types$/)
  })
  expect(p95).toBeLessThan(LIMIT_MS)
})

for (const [name, inputs, selector] of [
  ['completed', loadsCentralInputs, '[data-verdict]'],
  ['derived refusal', loadsContactRefusalInputs, '[data-status="refusal"]'],
] as const) {
  test(`loads submitted form to ${name}, including minimum computation, uses the same p95 policy`, async ({ page }) => {
    const p95 = await measure(page, async (current) => {
      await current.goto(`/calculations/new?type=${LOADS_TYPE}`)
      for (const [field, quantity] of Object.entries(inputs)) await current.locator(`#field-${field}`).fill(String(quantity.value))
      await current.evaluate((target) => window.__watch('loads-submitted', target), selector)
      await current.getByRole('button', { name: 'Рассчитать', exact: true }).click()
      await expect(current.locator(selector)).toBeVisible()
      return elapsed(current, 'loads-submitted', /\/calculations$/)
    })
    expect(p95).toBeLessThan(LIMIT_MS)
  })
}

for (const [name, id, selector] of [
  ['completed', loadsCentralEnvelope.result_id, '[data-verdict]'],
  ['derived refusal', loadsContactRefusalEnvelope.result_id, '[data-status="refusal"]'],
] as const) {
  test(`loads ${name} opened by its address uses the same p95 policy`, async ({ page }) => {
    const p95 = await measure(page, async (current) => {
      await current.goto('/nowhere')
      await current.evaluate((target) => window.__watch('loads-opened', target), selector)
      await current.evaluate((resultId) => {
        history.pushState({}, '', `/calculations/${resultId}`)
        dispatchEvent(new PopStateEvent('popstate'))
      }, id)
      await expect(current.locator(selector)).toBeVisible()
      return elapsed(current, 'loads-opened', /\/calculations\/[\w-]+$/)
    })
    expect(p95).toBeLessThan(LIMIT_MS)
  })
}

test('loads report POST to the issued stamp uses the same p95 policy', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto(`/calculations/${loadsCentralEnvelope.result_id}/report`)
    for (const [label, value] of Object.entries(REPORT)) await current.getByLabel(label, { exact: true }).fill(value)
    await current.evaluate(() => window.__watch('loads-report', '[data-report-stamp]'))
    await current.locator('form button[type="submit"]').click()
    await expect(current.locator('[data-report-stamp]')).toBeVisible()
    return elapsed(current, 'loads-report', /\/report$/)
  })
  expect(p95).toBeLessThan(LIMIT_MS)
})


test('design tools explicit check to result meets p95', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto('/calculations/new?type=foundations_shallow_weights')
    for (const [field, quantity] of Object.entries(weightsCentralRequest.inputs)) await current.locator(`#field-${field}`).fill(String(quantity.value))
    await current.evaluate(() => window.__watch('explicit-result', '[data-verdict]'))
    await current.getByRole('button', { name: 'Рассчитать', exact: true }).click()
    await expect(current.locator('[data-verdict]')).toBeVisible()
    return elapsed(current, 'explicit-result', /\/calculations$/)
  })
  console.log(`Explicit check transition p95: ${p95.toFixed(1)} ms`)
  expect(p95).toBeLessThan(LIMIT_MS)
})

test('design tools selection POST to stored comparison meets p95', async ({ page }) => {
  const p95 = await measure(page, async (current) => {
    await current.goto(`/calculations/new?type=${LOADS_TYPE}&task=selection`)
    for (const [field, quantity] of Object.entries(selectionSelected.request.common_inputs)) await current.locator(`#field-${field}`).fill(String(quantity.value))
    for (const [index, { b, l }] of selectionSelected.request.candidates.entries()) {
      if (index > 0) await current.getByRole('button', { name: 'Добавить вариант' }).click()
      await current.locator(`#candidate-${index}-b`).fill(String(b.value))
      await current.locator(`#candidate-${index}-l`).fill(String(l.value))
    }
    await current.evaluate(() => window.__watch('selection', '[data-candidate]'))
    await current.getByRole('button', { name: 'Подобрать размеры' }).click()
    await expect(current.locator('[data-candidate]').first()).toBeVisible()
    return elapsed(current, 'selection', /\/foundation-selections$/)
  })
  console.log(`Selection transition p95: ${p95.toFixed(1)} ms`)
  expect(p95).toBeLessThan(LIMIT_MS)
})
