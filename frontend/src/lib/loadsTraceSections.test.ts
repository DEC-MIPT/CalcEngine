import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { loadsCentralEnvelope, loadsContactRefusalEnvelope, passEnvelope } from '@/mocks/fixtures'
import { loadsTraceSections } from './loadsTraceSections'

type Step = components['schemas']['ResultEnvelope']['trace'][number]

const signature = ['A', 'Wx', 'Wy', 'Mx_base', 'My_base', 'p_corner_pp', 'p_corner_pm', 'p_corner_mp', 'p_corner_mm', 'p_corner_min']
const steps: readonly Step[] = loadsCentralEnvelope.trace

describe('conservative loads trace recognition', () => {
  it.each([loadsCentralEnvelope, loadsContactRefusalEnvelope])('recognizes stored complete and diagnostic prefixes without changing their data', (envelope) => {
    const before = structuredClone(envelope.trace)
    const sections = loadsTraceSections(envelope.trace)
    expect(sections).not.toBeNull()
    expect(sections).toHaveLength(envelope.trace.length)
    expect(envelope.trace).toEqual(before)
  })

  it.each(signature)('rejects an absent signature member %s', (id) => {
    expect(loadsTraceSections(steps.filter((step) => step.step_id !== id))).toBeNull()
  })

  it.each(signature)('rejects a duplicated signature member %s', (id) => {
    expect(loadsTraceSections([...steps, steps.find((step) => step.step_id === id)!])).toBeNull()
  })

  it.each(signature)('rejects a wrong-kind signature member %s', (id) => {
    const replacement: Step = { ...passEnvelope.trace[0], step_id: id }
    expect(loadsTraceSections(steps.map((step) => step.step_id === id ? replacement : step))).toBeNull()
  })

  it.each([[], passEnvelope.trace].map((trace) => ({ trace })))('leaves an unrecognized trace in the existing view', ({ trace }) => {
    expect(loadsTraceSections(trace)).toBeNull()
  })

  it('recognizes identifiers and kinds without using numerical equality or formula text', () => {
    const changed = steps.map((step) => ({ ...step, expression: 'unrelated stored expression', result: { ...step.result, value: 987.654 } }))
    expect(loadsTraceSections(changed)).toEqual(loadsTraceSections(steps))
  })

  it('retains unknown supplemental steps, including object-property names, at their original positions', () => {
    const additions = ['__proto__', 'constructor', 'unrecognized'].map((step_id) => ({ ...steps[0], step_id }))
    const supplemented = [...steps.slice(0, 3), ...additions, ...steps.slice(3)]
    const sections = loadsTraceSections(supplemented)!
    expect(sections.slice(3, 6)).toEqual(['other', 'other', 'other'])
    expect(sections.slice(0, 3)).toEqual(loadsTraceSections(steps)!.slice(0, 3))
    expect(sections.slice(6)).toEqual(loadsTraceSections(steps)!.slice(3))
  })

  it('does not synthesize missing non-signature members or move later sections', () => {
    const omitted = new Set(['p_x_min', 'p_x_max', 'e_x', 'relative_eccentricity_x', 'pressure_diagram_x'])
    const shortened = steps.filter((step) => !omitted.has(step.step_id))
    const sections = loadsTraceSections(shortened)!
    expect(sections).toHaveLength(shortened.length)
    expect(sections).not.toContain('x')
    expect(sections).toContain('y')
    expect(sections).toContain('checks')
  })
})
