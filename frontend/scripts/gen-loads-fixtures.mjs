import { execFileSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const backend = resolve(root, '..', 'backend')
const python = process.env.DEC_PYTHON ?? join(backend, '.venv', 'bin', 'python')
const exporter = readFileSync(join(root, 'scripts', 'export-loads-fixtures.py'), 'utf8')
const target = join(root, 'src', 'mocks', 'loadsFixtures.ts')
const generated = execFileSync(python, ['-c', exporter], { cwd: backend, encoding: 'utf8' })

if (process.argv.includes('--check')) {
  if (readFileSync(target, 'utf8') !== generated) {
    console.error('src/mocks/loadsFixtures.ts is out of date: run `node scripts/gen-loads-fixtures.mjs`')
    process.exitCode = 1
  }
} else {
  writeFileSync(target, generated)
}
