import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { expectNoA11yViolations } from '@/test/axe'
import { Formula } from './Formula'

describe('Formula', () => {
  it.each([
    String.raw`R = \frac{\gamma_{c1}}{k}`,
    String.raw`\varphi_{II}`,
    String.raw`\gamma'_{II}`,
    String.raw`R = \mathrm{synthetic}`,
    String.raw`p \le R`,
  ])('typesets %s as an SVG with the source as its name', (latex) => {
    render(<Formula latex={latex} />)

    const formula = screen.getByRole('img', { name: latex })
    expect(formula.querySelector('svg')).not.toBeNull()
    expect(document.querySelector('[data-fallback]')).toBeNull()
  })

  it('hides the inner SVG from assistive technology and has no accessibility violations', async () => {
    const { container } = render(<Formula latex={String.raw`p \le R`} />)

    expect(screen.getByRole('img', { name: String.raw`p \le R` }).firstElementChild).toHaveAttribute(
      'aria-hidden',
      'true',
    )
    await expectNoA11yViolations(container)
  })

  it('typesets a displayed formula', () => {
    render(<Formula latex="x^2" display />)

    expect(screen.getByRole('img', { name: 'x^2' }).querySelector('svg')).not.toBeNull()
  })

  it('shows the source of a string it cannot typeset and does not throw', () => {
    const { container } = render(<Formula latex={String.raw`\frac{1`} />)

    expect(container.querySelector('code[data-fallback="true"]')).toHaveTextContent(String.raw`\frac{1`)
    expect(container.querySelector('svg')).toBeNull()
  })

  it.each([
    String.raw`\href{javascript:alert(1)}{x}`,
    String.raw`\require{html}`,
    String.raw`\unicode{x41}`,
    String.raw`\class{evil}{x}`,
  ])('shows %s as inert text: no link, no script, no extension load', (latex) => {
    const { container } = render(<Formula latex={latex} />)

    expect(container.querySelector('code[data-fallback="true"]')).toHaveTextContent(latex)
    expect(container.querySelector('a, script, svg')).toBeNull()
  })

  it.each([
    String.raw`\mmlToken{mi}[href="javascript:alert(1)"]{x}`,
    String.raw`\mmlToken{mi}[href="https://example.com"]{x}`,
    String.raw`\mmlToken{mi}[style="position:fixed;inset:0;background:red"]{x}`,
    String.raw`\mmlToken{mi}[style="color:red"]{x}`,
    String.raw`\mmlToken{mi}[class="evil" id="evil"]{x}`,
  ])('drops the link, style, class and id that %s asks for', (latex) => {
    const { container } = render(<Formula latex={latex} />)

    const svg = container.querySelector('svg')

    expect(svg).not.toBeNull()
    expect(svg?.querySelector('a, [href], .evil, #evil')).toBeNull()
    expect(svg?.outerHTML).not.toMatch(/javascript:|example\.com|position:\s*fixed|color:\s*red/)
  })

  it('typesets again when the formula changes', () => {
    const { rerender } = render(<Formula latex="a" />)

    rerender(<Formula latex="b" />)

    expect(screen.getByRole('img', { name: 'b' }).querySelector('svg')).not.toBeNull()
    expect(screen.queryByRole('img', { name: 'a' })).toBeNull()
  })
})
