import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const harness = vi.hoisted(() => ({
  execute: vi.fn(),
  read: vi.fn(),
  write: vi.fn(),
}))

vi.mock('node:child_process', async (original) => {
  const actual = await original<typeof import('node:child_process')>()
  return { ...actual, execFileSync: harness.execute, default: { ...actual, execFileSync: harness.execute } }
})
vi.mock('node:fs', async (original) => {
  const actual = await original<typeof import('node:fs')>()
  const mocked = { ...actual, readFileSync: harness.read, writeFileSync: harness.write }
  return { ...mocked, default: mocked }
})

const originalArgs = process.argv
const originalExitCode = process.exitCode
const originalPython = process.env.DEC_PYTHON
const generated = 'export const capturedBackendResult = true\n'

beforeEach(() => {
  vi.resetModules()
  vi.clearAllMocks()
  process.argv = ['node', 'gen-loads-fixtures.mjs']
  process.exitCode = undefined
  delete process.env.DEC_PYTHON
  harness.execute.mockReturnValue(generated)
  harness.read.mockImplementation((path: string) =>
    path.endsWith('export-loads-fixtures.py') ? 'backend exporter source' : generated,
  )
})

afterEach(() => {
  process.argv = originalArgs
  process.exitCode = originalExitCode
  if (originalPython === undefined) delete process.env.DEC_PYTHON
  else process.env.DEC_PYTHON = originalPython
  vi.restoreAllMocks()
})

async function runGenerator() {
  await import('./gen-loads-fixtures.mjs')
}

describe('loads fixture generation command', () => {
  it('writes exactly backend stdout using the existing project interpreter', async () => {
    await runGenerator()

    expect(harness.execute).toHaveBeenCalledWith(
      expect.stringMatching(/backend\/\.venv\/bin\/python$/),
      ['-c', 'backend exporter source'],
      { cwd: expect.stringMatching(/backend$/), encoding: 'utf8' },
    )
    expect(harness.write).toHaveBeenCalledWith(
      expect.stringMatching(/src\/mocks\/loadsFixtures\.ts$/), generated,
    )
  })

  it('checks reproducible fixtures without rewriting them and honors DEC_PYTHON', async () => {
    process.argv.push('--check')
    process.env.DEC_PYTHON = '/test-only/python'
    const errors = vi.spyOn(console, 'error').mockImplementation(() => undefined)

    await runGenerator()

    expect(harness.execute.mock.calls[0][0]).toBe('/test-only/python')
    expect(harness.write).not.toHaveBeenCalled()
    expect(errors).not.toHaveBeenCalled()
    expect(process.exitCode).toBeUndefined()
  })

  it('fails drift checks explicitly without replacing the reviewed fixture', async () => {
    process.argv.push('--check')
    harness.read.mockImplementation((path: string) =>
      path.endsWith('export-loads-fixtures.py') ? 'backend exporter source' : 'stale fixture',
    )
    const errors = vi.spyOn(console, 'error').mockImplementation(() => undefined)

    await runGenerator()

    expect(process.exitCode).toBe(1)
    expect(errors).toHaveBeenCalledWith(expect.stringContaining('loadsFixtures.ts is out of date'))
    expect(harness.write).not.toHaveBeenCalled()
  })

  it('checks the generated design fixtures with the design exporter', async () => {
    process.argv.push('--design', '--check')
    harness.read.mockImplementation((path: string) => path.endsWith('export-design-fixtures.py') ? 'design exporter source' : 'stale')
    const errors = vi.spyOn(console, 'error').mockImplementation(() => undefined)

    await runGenerator()

    expect(harness.execute.mock.calls[0][1]).toEqual(['-c', 'design exporter source'])
    expect(harness.read).toHaveBeenCalledWith(expect.stringMatching(/src\/mocks\/designFixtures\.ts$/), 'utf8')
    expect(errors).toHaveBeenCalledWith(expect.stringContaining('designFixtures.ts is out of date'))
    expect(process.exitCode).toBe(1)
    expect(harness.write).not.toHaveBeenCalled()
  })

  it('propagates backend export failures without writing fabricated data', async () => {
    harness.execute.mockImplementation(() => {
      throw new Error('backend export failed')
    })

    await expect(runGenerator()).rejects.toThrow('backend export failed')
    expect(harness.write).not.toHaveBeenCalled()
  })
})
