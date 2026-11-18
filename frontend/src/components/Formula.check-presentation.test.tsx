import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { calculationTypes, loadsCentralEnvelope } from '@/mocks/fixtures'
import { checkPresentation } from '@/lib/checkPresentation'
import { symbolTable } from '@/lib/stepSymbol'
import { Formula } from './Formula'

const checks = loadsCentralEnvelope.trace.filter((step) => step.kind === 'check')
const symbols = symbolTable(loadsCentralEnvelope.trace, calculationTypes)

describe('auditable check expression presentation', () => {
  it.each(checks)('typesets $step_id while preserving its original accessible expression', (step) => {
    const { container } = render(<Formula latex={step.expression} presentation={checkPresentation(step, symbols)} />)
    const image = screen.getByRole('img', { name: step.expression })
    expect(image).toHaveAttribute('data-source-expression', step.expression)
    expect(image.querySelector('svg')).not.toBeNull()
    expect(image.querySelector('[data-c="2264"]')).not.toBeNull()
    expect(container.querySelector('[data-fallback]')).toBeNull()
  })

  it('fails closed to the original inert text when an alias is rejected', () => {
    const step = checks[0]
    const presentation = checkPresentation(step, new Map([['p', String.raw`\href{javascript:alert(1)}{p}`]]))
    const { container } = render(<Formula latex={step.expression} presentation={presentation} />)
    expect(container.querySelector('[data-fallback]')).toHaveTextContent(step.expression)
    expect(container.querySelector('a, script, svg')).toBeNull()
    expect(screen.queryByRole('img')).not.toBeInTheDocument()
  })

  it('keeps an unexpected hostile original inert instead of repairing it', () => {
    const step = { ...checks[0], expression: String.raw`\href{javascript:alert(1)}{p}` }
    const { container } = render(<Formula latex={step.expression} presentation={checkPresentation(step, symbols)} />)
    expect(container.querySelector('[data-fallback]')).toHaveAttribute('data-source-expression', step.expression)
    expect(container.querySelector('a, script, svg')).toBeNull()
  })
})
