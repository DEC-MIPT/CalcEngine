import { expect, test, type Page } from '@playwright/test'

const PASS_ID = '11111111-1111-4111-8111-111111111111'
const UNKNOWN_ID = '99999999-9999-4999-8999-999999999999'

const FIELDS = {
  'Обозначение документа': 'ДЕК-2026-001-РР',
  'Наименование документа': 'Расчёт сопротивления грунта',
  Организация: 'ООО «Проект»',
  'Разработал: Фамилия': 'Иванов',
  'Разработал: Дата': '2026-10-07',
  'Нормоконтроль: Фамилия': 'Петрова',
  'Нормоконтроль: Дата': '2026-10-08',
}

async function openFilled(page: Page, id = PASS_ID) {
  await page.goto(`/calculations/${id}/report`)
  for (const [label, value] of Object.entries(FIELDS)) {
    await page.getByLabel(label, { exact: true }).fill(value)
  }
}

function countReportRequests(page: Page) {
  const sent: string[] = []
  page.on('request', (request) => {
    if (request.method() === 'POST' && request.url().endsWith('/report')) sent.push(request.url())
  })
  return sent
}

const submitButton = (page: Page) => page.locator('form button[type="submit"]')
const stamp = (page: Page) => page.locator('[data-report-stamp]')
const animationOf = (page: Page, selector: string) =>
  page.locator(selector).evaluate((node) => getComputedStyle(node).animationName)

test.use({
  viewport: { width: 1280, height: 900 },
  video: { mode: 'on', size: { width: 1280, height: 900 } },
})

test.describe('recorded', () => {
  test.skip(({ browserName }) => browserName !== 'chromium', 'the report flow is recorded in Chromium')
  test.use({ reducedMotion: 'no-preference' })

  test('the button turns busy, the title block is stamped, and the .docx downloads', async ({ page }, info) => {
    await openFilled(page)
    await page.screenshot({ path: info.outputPath('success-1-idle.png') })

    await submitButton(page).click()
    await expect(submitButton(page)).toHaveAttribute('aria-busy', 'true')
    await expect(page.locator('[data-report-status]')).toHaveText('Формирование отчёта…')
    await page.screenshot({ path: info.outputPath('success-2-busy.png') })

    await expect(stamp(page)).toBeVisible()
    await expect(stamp(page)).toHaveAttribute('data-strike', 'animated')
    expect(await animationOf(page, '[data-report-stamp]')).toBe('report-strike, report-ink')
    expect(await animationOf(page, 'form')).toBe('report-jolt')
    await page.waitForTimeout(400)
    await page.screenshot({ path: info.outputPath('success-3-stamp.png') })
    await expect(submitButton(page)).toHaveText('Отчёт сформирован')
    await expect(page.getByRole('button', { name: 'Скачать report.docx' })).toBeFocused()

    const download = page.waitForEvent('download')
    await page.keyboard.press('Enter')
    expect((await download).suggestedFilename()).toBe('report.docx')
    await expect(page.locator('[data-report-status]')).toHaveText('Отчёт сохранён: report.docx')
    await page.screenshot({ path: info.outputPath('success-4-saved.png') })
    await page.waitForTimeout(600)
  })

  test('a failed report shows its error and a retry, with no stamp and no jolt', async ({ page }, info) => {
    await openFilled(page, UNKNOWN_ID)

    await submitButton(page).click()
    const alert = page.getByRole('alert')
    await expect(alert).toContainText('not_found')
    await expect(alert.getByRole('button', { name: 'Повторить' })).toBeVisible()
    await expect(stamp(page)).toHaveCount(0)
    expect(await animationOf(page, 'form')).toBe('none')
    await expect(submitButton(page)).toHaveText('Сформировать отчёт')
    await expect(submitButton(page)).not.toHaveAttribute('aria-disabled')
    await page.screenshot({ path: info.outputPath('error-1-alert.png') })
    await page.waitForTimeout(800)
  })
})

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' })

  test('the stamp appears at once, without the strike or the jolt', async ({ page }) => {
    await openFilled(page)

    await submitButton(page).click()

    await expect(stamp(page)).toBeVisible()
    await expect(stamp(page)).toHaveAttribute('data-strike', 'instant')
    expect(await animationOf(page, '[data-report-stamp]')).toBe('none')
    expect(await animationOf(page, 'form')).toBe('none')
  })
})

test.describe('one report at a time', () => {
  test.use({ reducedMotion: 'no-preference' })

  test('clicks and Enter while the report is built send no second request', async ({ page }) => {
    const sent = countReportRequests(page)
    await openFilled(page)

    await submitButton(page).click()
    await expect(submitButton(page)).toHaveAttribute('aria-busy', 'true')
    await submitButton(page).dblclick({ force: true })
    await page.getByLabel('Организация', { exact: true }).press('Enter')

    await expect(stamp(page)).toBeVisible()
    await page.waitForTimeout(300)
    expect(sent).toHaveLength(1)
    await expect(stamp(page)).toHaveCount(1)
  })
})
