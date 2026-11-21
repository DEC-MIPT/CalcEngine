import type { components } from '@/api/schema'

type Step = components['schemas']['ResultEnvelope']['trace'][number]

export type LoadsTraceSection = 'resistance' | 'geometry' | 'mean' | 'x' | 'y' | 'corners' | 'contact' | 'checks' | 'other'

const SIGNATURE = ['A', 'Wx', 'Wy', 'Mx_base', 'My_base', 'p_corner_pp', 'p_corner_pm', 'p_corner_mp', 'p_corner_mm', 'p_corner_min']

const SECTIONS = new Map<string, LoadsTraceSection>([
  ...['gamma_c1', 'gamma_c2', 'k', 'M_gamma', 'M_q', 'M_c', 'k_z', 'R'].map((id) => [id, 'resistance'] as const),
  ...['A', 'Wx', 'Wy', 'Mx_base', 'My_base'].map((id) => [id, 'geometry'] as const),
  ...['gamma_mt', 'p', 'V'].map((id) => [id, 'mean'] as const),
  ...['p_x_min', 'p_x_max', 'e_x', 'relative_eccentricity_x', 'pressure_diagram_x'].map((id) => [id, 'x'] as const),
  ...['p_y_min', 'p_y_max', 'e_y', 'relative_eccentricity_y', 'pressure_diagram_y'].map((id) => [id, 'y'] as const),
  ...['pp', 'pm', 'mp', 'mm'].flatMap((suffix) => [
    [`corner_component_${suffix}`, 'corners'] as const,
    [`p_corner_${suffix}`, 'corners'] as const,
  ]),
  ...['p_corner_min', 'p_corner_max'].map((id) => [id, 'contact'] as const),
  ...['edge_limit_multiplier', 'edge_limit', 'corner_limit_multiplier', 'corner_limit', 'p_le_R', 'p_x_max_le_limit', 'p_y_max_le_limit', 'p_corner_max_le_limit'].map((id) => [id, 'checks'] as const),
])

export function loadsTraceSections(steps: readonly Step[]): readonly LoadsTraceSection[] | null {
  if (SIGNATURE.some((id) => {
    const matches = steps.filter((step) => step.step_id === id)
    return matches.length !== 1 || matches[0].kind !== 'engineer_formula'
  })) return null
  return steps.map((step) => SECTIONS.get(step.step_id) ?? 'other')
}
