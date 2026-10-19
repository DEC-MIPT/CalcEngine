import axe from 'axe-core'

export async function expectNoA11yViolations(container: Element): Promise<void> {
  const { violations } = await axe.run(container, {
    rules: { 'color-contrast': { enabled: false } },
  })
  if (violations.length > 0) {
    const report = violations.map(
      (violation) =>
        `${violation.id}: ${violation.help} (${violation.nodes.map((node) => node.target.join(' ')).join(', ')})`,
    )
    throw new Error(`Accessibility violations:\n${report.join('\n')}`)
  }
}
