import { createRequire } from 'node:module'
import { expect, test, type Page } from '@playwright/test'

const PASS_ID = '11111111-1111-4111-8111-111111111111'
const FAIL_ID = '22222222-2222-4222-8222-222222222222'
const REFUSED_ID = '33333333-3333-4333-8333-333333333333'
const WARNING_ID = '44444444-4444-4444-8444-444444444444'
const AXE = createRequire(import.meta.url).resolve('axe-core/axe.min.js')

const INPUTS = { b: '2', d_1: '1.5', d_b: '0', gamma_II: '18', gamma_II_prime: '18', c_II: '10', phi_II: '20', p: '100' }
const REPORT_TEXT = {
  'Обозначение документа': 'ДЕК-2026-001-РР',
  'Наименование документа': 'Расчёт сопротивления грунта',
  Организация: 'ООО «Проект»',
  'Разработал: Фамилия': 'Иванов',
  'Нормоконтроль: Фамилия': 'Петрова',
}
const REPORT_DATES = { 'Разработал: Дата': '10072026', 'Нормоконтроль: Дата': '10082026' }

test.skip(({ browserName }) => browserName !== 'chromium', 'the keyboard journey and the contrast check run in Chromium')
test.use({ reducedMotion: 'reduce', viewport: { width: 1280, height: 900 }, locale: 'en-US' })

type Indicator = { visible: boolean; ratio: number; target: string; detail: string }

async function focusIndicator(page: Page): Promise<Indicator | null> {
  return page.evaluate(() => {
    const element = document.activeElement as HTMLElement | null
    if (!element || element === document.body) return null
    const channel = (value: number) => {
      const unit = value / 255
      return unit <= 0.04045 ? unit / 12.92 : ((unit + 0.055) / 1.055) ** 2.4
    }
    const parse = (color: string) => {
      const [r, g, b, a = 1] = color.match(/[\d.]+/g)!.map(Number)
      return { r, g, b, a }
    }
    const luminance = ({ r, g, b }: { r: number; g: number; b: number }) =>
      0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)
    const backgroundOf = (start: Element) => {
      for (let node: Element | null = start; node; node = node.parentElement) {
        const style = getComputedStyle(node)
        const gradient = style.backgroundImage.match(/rgba?\([^)]*\)/)
        if (gradient && style.backgroundSize.startsWith('100%')) return parse(gradient[0])
        const color = parse(style.backgroundColor)
        if (color.a > 0) return color
      }
      return { r: 255, g: 255, b: 255, a: 1 }
    }
    const style = getComputedStyle(element)
    const visible = style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) >= 2
    const ring = luminance(parse(style.outlineColor))
    const inside = parseFloat(style.outlineOffset) < 0
    const behind = luminance(backgroundOf(inside ? element : (element.parentElement ?? element)))
    const ratio = (Math.max(ring, behind) + 0.05) / (Math.min(ring, behind) + 0.05)
    const target = `${element.tagName.toLowerCase()} ${element.getAttribute('aria-label') ?? element.id ?? ''} ${element.textContent?.trim().slice(0, 40) ?? ''}`
    const detail = `${style.outlineStyle} ${style.outlineWidth} ${style.outlineColor} offset ${style.outlineOffset}`
    return { visible, ratio, target, detail }
  })
}

async function press(page: Page, key: string, seen: Indicator[]) {
  await page.keyboard.press(key)
  await page.waitForTimeout(200)
  const indicator = await focusIndicator(page)
  if (indicator) {
    seen.push(indicator)
    expect.soft(indicator.visible, `focus indicator on ${indicator.target} (${indicator.detail})`).toBe(true)
    expect.soft(indicator.ratio, `focus contrast on ${indicator.target} (${indicator.detail}, ${indicator.ratio.toFixed(2)})`).toBeGreaterThanOrEqual(3)
  }
}

async function tabUntil(page: Page, matches: (page: Page) => Promise<boolean>, seen: Indicator[], limit = 60) {
  for (let step = 0; step < limit; step += 1) {
    await press(page, 'Tab', seen)
    if (await matches(page)) return
  }
  throw new Error('the target was not reached by Tab')
}

const focusedIs = (selector: string) => (page: Page) => page.locator(selector).evaluate((node) => node === document.activeElement)
const focusedLabel = (label: string) => (page: Page) =>
  page.getByLabel(label, { exact: true }).evaluate((node) => node === document.activeElement)

test('the journey from type selection to the downloaded report completes with the keyboard alone (8.6)', async ({ page }) => {
  test.setTimeout(120_000)
  const seen: Indicator[] = []
  await page.goto('/')
  await expect(page.getByRole('link', { name: /Расчётное сопротивление грунта/ })).toBeVisible()

  await tabUntil(page, (current) => current.getByRole('link', { name: /Расчётное сопротивление грунта/ }).evaluate((node) => node === document.activeElement), seen)
  await press(page, 'Enter', seen)
  await expect(page.locator('#field-b')).toBeVisible()

  for (const [name, value] of Object.entries(INPUTS)) {
    await tabUntil(page, focusedIs(`#field-${name}`), seen)
    await page.keyboard.type(value)
  }
  await tabUntil(page, (current) => current.getByRole('button', { name: 'Рассчитать' }).evaluate((node) => node === document.activeElement), seen)
  await press(page, 'Enter', seen)
  await expect(page.locator('[data-verdict]')).toBeFocused()

  await tabUntil(page, (current) => current.getByRole('link', { name: 'Запросить отчёт' }).evaluate((node) => node === document.activeElement), seen)
  await press(page, 'Enter', seen)
  await expect(page.getByLabel('Обозначение документа', { exact: true })).toBeVisible()

  for (const [label, value] of Object.entries(REPORT_TEXT)) {
    await tabUntil(page, focusedLabel(label), seen)
    await page.keyboard.type(value)
  }
  for (const [label, value] of Object.entries(REPORT_DATES)) {
    await tabUntil(page, focusedLabel(label), seen)
    await page.keyboard.type(value)
  }
  await tabUntil(page, focusedIs('form button[type="submit"]'), seen)
  await press(page, 'Enter', seen)
  await expect(page.locator('[data-report-stamp]')).toBeVisible()

  await tabUntil(page, (current) => current.getByRole('button', { name: /^Скачать/ }).evaluate((node) => node === document.activeElement), seen)
  const download = page.waitForEvent('download')
  await page.keyboard.press('Enter')
  expect((await download).suggestedFilename()).toMatch(/\.docx$/)
  expect(seen.length).toBeGreaterThan(20)
})

async function contrastViolations(page: Page) {
  await page.addScriptTag({ path: AXE })
  return page.evaluate(async () => {
    const result = await (window as unknown as { axe: { run: (context: Document, options: object) => Promise<{ violations: { nodes: { target: string[] }[] }[] }> } }).axe.run(document, {
      runOnly: { type: 'rule', values: ['color-contrast'] },
    })
    return result.violations.flatMap((violation) => violation.nodes.map((node) => node.target.join(' ')))
  })
}

const SCREENS: [string, string, (page: Page) => Promise<void>][] = [
  ['type selection', '/', (page) => expect(page.getByRole('link', { name: /Расчётное сопротивление грунта/ })).toBeVisible()],
  ['input form', '/calculations/new?type=foundations_shallow_r', (page) => expect(page.locator('#field-b')).toBeVisible()],
  ['result: pass', `/calculations/${PASS_ID}`, (page) => expect(page.locator('[data-verdict]')).toBeVisible()],
  ['result: fail', `/calculations/${FAIL_ID}`, (page) => expect(page.locator('[data-verdict]')).toBeVisible()],
  ['result: warning', `/calculations/${WARNING_ID}`, (page) => expect(page.getByRole('region', { name: /^Предупреждение/ })).toBeVisible()],
  ['result: refusal', `/calculations/${REFUSED_ID}`, (page) => expect(page.getByRole('region', { name: /^Расчёт не выполнен/ })).toBeVisible()],
  ['result: not found', '/calculations/99999999-9999-4999-8999-999999999999', (page) => expect(page.getByRole('heading', { name: 'Результат не найден' })).toBeVisible()],
  ['report request', `/calculations/${PASS_ID}/report`, (page) => expect(page.getByLabel('Обозначение документа', { exact: true })).toBeVisible()],
  ['page not found', '/nowhere', (page) => expect(page.getByRole('link', { name: 'Типы расчётов' })).toBeVisible()],
]

for (const [name, address, ready] of SCREENS) {
  test(`no text below the contrast threshold on ${name} (8.7)`, async ({ page }) => {
    await page.goto(address)
    await ready(page)

    expect(await contrastViolations(page)).toEqual([])
  })
}

test('no text below the contrast threshold on the form and the report with their marks and the echo (8.7)', async ({ page }) => {
  await page.goto('/calculations/new?type=foundations_shallow_r')
  await page.locator('#field-b').fill('200')
  await page.getByLabel(/^Единица: Ширина подошвы/).selectOption('cm')
  await page.getByRole('button', { name: 'Рассчитать' }).click()
  await expect(page.getByText('Введите значение.').first()).toBeVisible()
  expect(await contrastViolations(page)).toEqual([])

  await page.goto(`/calculations/${PASS_ID}/report`)
  await page.locator('form button[type="submit"]').click()
  await expect(page.getByText('Заполните поле.').first()).toBeVisible()
  expect(await contrastViolations(page)).toEqual([])
})

test('no text below the contrast threshold on the issued report stamp (8.7)', async ({ page }) => {
  await page.goto(`/calculations/${PASS_ID}/report`)
  for (const [label, value] of Object.entries(REPORT_TEXT)) {
    await page.getByLabel(label, { exact: true }).fill(value)
  }
  await page.getByLabel('Разработал: Дата', { exact: true }).fill('2026-10-07')
  await page.getByLabel('Нормоконтроль: Дата', { exact: true }).fill('2026-10-08')
  await page.locator('form button[type="submit"]').click()
  await expect(page.locator('[data-report-stamp]')).toBeVisible()

  expect(await contrastViolations(page)).toEqual([])
})
