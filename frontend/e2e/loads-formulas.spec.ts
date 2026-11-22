import { expect, test, type Locator } from '@playwright/test'
import { loadsCalculationType, loadsCentralEnvelope, loadsScenarios } from '../src/mocks/loadsFixtures'

const RELATION_GLYPHS = { le: '2264', lt: '3C', ge: '2265', gt: '3E' } as const

async function subscriptGroups(formula: Locator) {
  return formula.locator('svg [data-mml-node="msub"]').evaluateAll((nodes) => nodes.map((node) => {
    const glyphs = (element: Element) => [...element.querySelectorAll('[data-c]')]
      .map((glyph) => String.fromCodePoint(Number.parseInt(glyph.getAttribute('data-c')!, 16)))
      .join('').normalize('NFKD')
    const [base, subscript] = [...node.children]
    return { base: glyphs(base), subscript: glyphs(subscript) }
  }))
}

test.use({ reducedMotion: 'reduce', viewport: { width: 1280, height: 900 } })

for (const scenario of loadsScenarios.filter((item) => item.envelope.trace.length > 0)) {
  test(`every actual ${scenario.name} loads trace expression typesets without raw fallback`, async ({ page }) => {
    const errors: string[] = []
    page.on('pageerror', (error) => errors.push(error.message))
    await page.goto(`/calculations/${scenario.envelope.result_id}`)
    const rows = page.locator('[data-step]')
    await expect(rows).toHaveCount(scenario.envelope.trace.length)
    expect(await rows.evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-step')))).toEqual(scenario.envelope.trace.map((step) => step.step_id))
    await page.getByRole('button', { name: 'Развернуть все шаги', exact: true }).click()

    const failures: { step: string; rendered: number; fallback: string | null }[] = []
    for (const step of scenario.envelope.trace) {
      const formula = page.locator(`[data-step="${step.step_id}"] .step-details > [role="region"]`).first()
      const rendered = await formula.locator('[role="img"] svg').count()
      const fallback = await formula.locator('[data-fallback]').count() ? await formula.locator('[data-fallback]').textContent() : null
      if (rendered !== 1 || fallback !== null) failures.push({ step: step.step_id, rendered, fallback })
      if (rendered === 1) await expect(formula.getByRole('img')).toHaveAttribute('aria-label', step.expression)
      if (step.kind === 'check' && rendered === 1) {
        await expect(formula.locator(`svg [data-mml-node="mo"] [data-c="${RELATION_GLYPHS[step.operator]}"]`)).toHaveCount(1)
        const groups = await subscriptGroups(formula)
        for (const operand of step.substitutions) {
          const declaration = loadsCalculationType.outputs.find((output) => output.name === operand.symbol)
          const definingStep = scenario.envelope.trace.find((item) => item.step_id === operand.symbol)
          const alias = declaration?.symbol ?? definingStep?.expression.split('=')[0].trim()
          const grouped = alias?.match(/^([A-Za-z]+)_\{([A-Za-z0-9,+-]+)\}$/)
          if (grouped) {
            expect(groups, `subscript grouping for ${operand.symbol} in ${step.step_id}`).toContainEqual({ base: grouped[1], subscript: grouped[2] })
          }
        }
      }
    }
    expect(failures, 'normal stored expressions must render as math in every supported browser').toEqual([])
    expect(errors).toEqual([])
  })
}

test('a hostile synthetic checked expression stays inert instead of being laundered into normal math', async ({ page }) => {
  const hostile = String.raw`\href{javascript:window.__unsafeFormulaExecuted=1}{attack}`
  const envelope = {
    ...loadsCentralEnvelope,
    trace: loadsCentralEnvelope.trace.map((step) => step.step_id === 'p_le_R' ? { ...step, expression: hostile } : step),
  }
  await page.addInitScript(({ stored }) => {
    const original = window.fetch.bind(window)
    window.fetch = async (...args: Parameters<typeof fetch>) => {
      const input = args[0]
      const url = new URL(input instanceof Request ? input.url : String(input), window.location.origin)
      if (url.pathname === `/calculations/${stored.result_id}`) {
        return new Response(JSON.stringify(stored), { headers: { 'Content-Type': 'application/json' } })
      }
      return original(...args)
    }
  }, { stored: envelope })
  await page.goto(`/calculations/${envelope.result_id}`)
  await page.getByRole('button', { name: 'Развернуть все шаги', exact: true }).click()
  const traceFormula = page.locator('[data-step="p_le_R"] .step-details > [role="region"]').first()
  await expect(traceFormula.locator('[data-fallback]')).toHaveText(hostile)
  await expect(traceFormula.locator('[role="img"]')).toHaveCount(0)
  await expect(page.locator('a[href^="javascript:"]')).toHaveCount(0)
  expect(await page.evaluate(() => Reflect.get(window, '__unsafeFormulaExecuted'))).toBeUndefined()
})
