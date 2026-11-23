import { readFile } from 'node:fs/promises'
import { expect, test, type Page } from '@playwright/test'
import type { components } from '../src/api/schema'
import {
  LOADS_TYPE,
  loadsBiaxialEnvelope,
  loadsBiaxialInputs,
  loadsCalculationType,
  loadsCentralEnvelope,
  loadsCentralInputs,
  loadsContactRefusalEnvelope,
  loadsContactRefusalInputs,
  loadsScenarios,
} from '../src/mocks/loadsFixtures'

type Inputs = components['schemas']['CalculationRequest']['inputs']
type Envelope = components['schemas']['ResultEnvelope']

const FORM = `/calculations/new?type=${LOADS_TYPE}`
const EDIT = 'Изменить исходные данные'
const REPORT = 'Запросить отчёт'
const REPORT_FIELDS = {
  'Обозначение документа': 'ДЕК-2026-LOADS-РР',
  'Наименование документа': 'Расчёт давления по нагрузкам',
  Организация: 'ООО «Проект»',
  'Разработал: Фамилия': 'Иванов',
  'Разработал: Дата': '2026-11-18',
  'Нормоконтроль: Фамилия': 'Петрова',
  'Нормоконтроль: Дата': '2026-11-18',
}

test.use({ reducedMotion: 'reduce', viewport: { width: 1280, height: 900 } })

async function fillInputs(page: Page, inputs: Inputs) {
  await expect(page.locator('#field-Qy')).toBeVisible()
  for (const [name, quantity] of Object.entries(inputs)) {
    const field = page.locator(`#field-${name}`)
    const unit = field.locator('..').locator('select')
    if (await unit.count()) await unit.selectOption(quantity.unit)
    await field.fill(String(quantity.value))
  }
}

async function submit(page: Page, id: string) {
  const response = page.waitForResponse((item) => item.request().method() === 'POST' && new URL(item.url()).pathname === '/calculations')
  await page.getByRole('button', { name: 'Рассчитать', exact: true }).click()
  const stored = await response
  expect(stored.status()).toBe(201)
  expect(stored.headers().location).toBe(`/calculations/${id}`)
  await expect(page).toHaveURL(new RegExp(`/calculations/${id}$`))
  return stored
}

async function inspectResult(page: Page, envelope: Envelope) {
  const refused = envelope.verdict === 'refused'
  const frame = page.locator(refused ? '[data-status="refusal"]' : '[data-verdict]')
  await expect(frame).toBeFocused()
  const source = frame.locator('[data-source="interim"]')
  await expect(source).toHaveAttribute('data-profile', 'strict')
  await expect(source).toContainText('ВРЕМЕННЫЕ ДАННЫЕ')
  await expect(source.locator('[title]')).toHaveAttribute('title', envelope.parameter_source!.data_sha256!)
  await expect(page.locator('[data-arrival="pending"]')).toHaveCount(0)
  await expect(page.getByRole('link', { name: EDIT, exact: true })).toBeVisible()

  if (envelope.verdict_reason.kind === 'check') {
    await expect(frame).toHaveAttribute('data-verdict', envelope.verdict)
    await expect(frame).toHaveAttribute('data-reveal', 'none')
    expect(await page.locator('[data-output]').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-output')))).toEqual(envelope.outputs.map((item) => item.quantity))
    const checks = envelope.trace.filter((step) => step.kind === 'check')
    expect(checks).toHaveLength(4)
    expect(await page.locator('[data-check-step]').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-check-step')))).toEqual(checks.map((step) => step.step_id))
    await expect(page.locator('[data-check-step][data-deciding="true"]')).toHaveAttribute('data-check-step', envelope.verdict_reason.step_id)
    for (const step of checks) {
      await expect(page.locator(`[data-check-step="${step.step_id}"]`).getByText(step.passed ? 'Проверка выполнена' : 'Проверка не выполнена', { exact: true })).toBeVisible()
    }
    for (const output of envelope.outputs) {
      await expect(page.locator(`[data-output="${output.quantity}"] [data-value]`)).toHaveText(output.value.toFixed(output.rounding_rule.decimals).replace('.', ','))
    }
  } else {
    await expect(page.locator('[data-output], [data-verdict], [data-check-step]')).toHaveCount(0)
    await expect(page.locator('.stamp-celebrate, .stamp-mark, [data-reveal="pending"]')).toHaveCount(0)
    if (envelope.verdict_reason.kind === 'derived') {
      const trace = page.getByRole('region', { name: 'Диагностическая последовательность', exact: true })
      await expect(trace).toHaveAttribute('data-playback', 'idle')
      expect(await trace.locator('[data-step]').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-step')))).toEqual(envelope.trace.map((step) => step.step_id))
      await expect(frame).toContainText(envelope.verdict_reason.limiting_corner)
      await expect(frame).toContainText('Проверки несущей способности не выполнялись')
    } else {
      await expect(page.locator('[data-step]')).toHaveCount(0)
      await expect(frame).toContainText(envelope.verdict_reason.bound.quantity)
    }
  }
}

async function downloadMockReport(page: Page) {
  await page.getByRole('link', { name: REPORT, exact: true }).click()
  for (const [name, value] of Object.entries(REPORT_FIELDS)) {
    await page.getByLabel(name, { exact: true }).fill(value)
  }
  await page.locator('form button[type="submit"]').click()
  const download = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Скачать report.docx', exact: true }).click()
  const file = await download
  expect(file.suggestedFilename()).toBe('report.docx')
  expect([...await readFile((await file.path())!)]).toEqual([0x50, 0x4b, 0x03, 0x04])
}

for (const scenario of loadsScenarios) {
  test(`captured loads ${scenario.name}: type, form, stored result and mock report download`, async ({ page }) => {
    const errors: string[] = []
    page.on('pageerror', (error) => errors.push(error.message))
    await page.goto(FORM)
    await expect(page.getByRole('textbox')).toHaveCount(15)
    expect(await page.getByRole('textbox').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('name')))).toEqual(loadsCalculationType.inputs.map((input) => input.name))
    await expect(page.getByRole('region', { name: 'Схема направлений и знаков', exact: true })).toBeVisible()
    await fillInputs(page, scenario.inputs)
    const response = await submit(page, scenario.envelope.result_id)
    expect(response.request().postDataJSON()).toEqual({ calculation_type: LOADS_TYPE, inputs: scenario.inputs })
    expect(await response.json()).toEqual(JSON.parse(scenario.json))
    await inspectResult(page, scenario.envelope)
    await downloadMockReport(page)
    expect(errors).toEqual([])
  })
}

test('derived correction preserves private raw drafts and becomes ineligible after a newer result', async ({ page }) => {
  await page.goto(FORM)
  await fillInputs(page, loadsContactRefusalInputs)
  await page.locator('#field-N').fill('+0600.000')
  await page.locator('#field-Mx').fill('+180000.000')
  await page.locator('#field-Mx').locator('..').locator('select').selectOption('N*m')
  await submit(page, loadsContactRefusalEnvelope.result_id)
  await page.getByRole('link', { name: EDIT, exact: true }).click()
  await expect(page.locator('#field-N')).toBeFocused()
  await expect(page.locator('#field-N')).toHaveValue('+0600.000')
  await expect(page.locator('#field-Mx')).toHaveValue('+180000.000')
  await expect(page.locator('#field-Mx').locator('..').locator('select')).toHaveValue('N*m')
  await expect(page.locator('#field-N')).toHaveAccessibleDescription(/p_corner_min: -30 кПа/)
  await expect(page.locator('#field-p_corner_min')).toHaveCount(0)
  expect(await page.evaluate(() => localStorage.length + sessionStorage.length)).toBe(0)
  const navigation = await page.evaluate(() => ({ url: window.location.href, state: history.state }))
  expect(JSON.stringify(navigation)).not.toContain('+0600.000')
  expect(JSON.stringify(navigation)).not.toContain('+180000.000')

  await fillInputs(page, loadsCentralInputs)
  await expect(page.locator('#field-N')).not.toHaveAccessibleDescription(/p_corner_min/)
  await submit(page, loadsCentralEnvelope.result_id)
  await expect(page.locator('[data-verdict]')).toBeFocused()
  await page.goBack()
  await expect(page.locator('#field-N')).toHaveValue(String(loadsCentralInputs.N.value))
  await page.goBack()
  await expect(page.locator('[data-status="refusal"]')).toBeVisible()
  await expect(page.getByRole('link', { name: EDIT, exact: true })).toHaveCount(0)
  await page.reload()
  await expect(page.locator('[data-status="refusal"]')).toBeVisible()
  await expect(page.getByRole('link', { name: EDIT, exact: true })).toHaveCount(0)
})

test('loads type, fifteen fields, result and report request remain reachable with the keyboard', async ({ page }) => {
  async function tabTo(selector: string) {
    const target = page.locator(selector)
    for (let count = 0; count < 80; count++) {
      if (await target.evaluate((element) => element === document.activeElement)) return
      await page.keyboard.press('Tab')
    }
    throw new Error(`Keyboard did not reach ${selector}`)
  }

  await page.goto('/')
  const demo = 'a[href="/calculations/new?type=foundations_shallow_weights"]'
  await expect(page.getByRole('link', { name: 'Расчет фундамента мелкого заложения (демо)', exact: true })).toBeVisible()
  await expect(page.locator(`a[href="${FORM}"]`)).toHaveCount(0)
  await tabTo(demo)
  await page.keyboard.press('Enter')
  const averaged = `a[href="${FORM}"]`
  await expect(page.locator(averaged)).toBeVisible()
  await tabTo(averaged)
  await page.keyboard.press('Enter')
  await expect(page).toHaveURL(new RegExp(`${LOADS_TYPE}$`))
  await expect(page.locator('#field-d')).toBeVisible()
  for (const [name, quantity] of Object.entries(loadsBiaxialInputs)) {
    const selector = `#field-${name}`
    await tabTo(selector)
    await page.keyboard.type(String(quantity.value))
    await expect(page.locator(selector)).toHaveValue(String(quantity.value))
  }
  await tabTo('form button[type="submit"]')
  await page.keyboard.press('Enter')
  await expect(page).toHaveURL(new RegExp(`/calculations/${loadsBiaxialEnvelope.result_id}$`))
  await expect(page.locator('[data-verdict]')).toBeFocused()
  await tabTo(`a[href="/calculations/${loadsBiaxialEnvelope.result_id}/report"]`)
  await page.keyboard.press('Enter')
  await expect(page.getByLabel('Обозначение документа', { exact: true })).toBeVisible()
})
