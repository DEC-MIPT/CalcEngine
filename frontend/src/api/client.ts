import createClient, { type ClientOptions } from 'openapi-fetch'
import type { components, paths } from './schema'

export type ErrorBody = components['schemas']['ErrorBody']
export type FieldError = components['schemas']['FieldError']

export type ApiError =
  | { kind: 'api'; status: number; code: string; message: string; fields: FieldError[] }
  | { kind: 'network' }

export type ApiResult<T> = { ok: true; data: T } | { ok: false; error: ApiError }

const DEFAULT_BASE_URL = 'http://127.0.0.1:8000'

export function createApi(options: ClientOptions = {}) {
  return createClient<paths>({
    baseUrl: import.meta.env.VITE_API_BASE_URL ?? DEFAULT_BASE_URL,
    fetch: (request) => globalThis.fetch(request),
    ...options,
  })
}

export const api = createApi()

function isErrorBody(value: unknown): value is ErrorBody {
  if (typeof value !== 'object' || value === null) return false
  const body = value as Record<string, unknown>
  return typeof body.code === 'string' && typeof body.message === 'string'
}

export async function unwrap<T>(
  request: Promise<{ data?: T; error?: unknown; response: Response }>,
): Promise<ApiResult<T>> {
  let outcome
  try {
    outcome = await request
  } catch {
    return { ok: false, error: { kind: 'network' } }
  }
  if (outcome.error === undefined) {
    return { ok: true, data: outcome.data as T }
  }
  return { ok: false, error: errorOf(outcome.error, outcome.response.status) }
}

export function errorOf(body: unknown, status: number): ApiError {
  if (isErrorBody(body)) {
    const { code, message, fields } = body
    return { kind: 'api', status, code, message, fields: fields ?? [] }
  }
  return { kind: 'api', status, code: 'unexpected_response', message: 'Unexpected response', fields: [] }
}
