import { execFileSync } from 'node:child_process'
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const backend = resolve(root, '..', 'backend')
const python = process.env.DEC_PYTHON ?? join(backend, '.venv', 'bin', 'python')
const target = join(root, 'src', 'api', 'schema.d.ts')
const check = process.argv.includes('--check')

const dump = 'import json; from app.main import create_app; print(json.dumps(create_app().openapi()))'
const scratch = mkdtempSync(join(tmpdir(), 'dec-openapi-'))
try {
  const schema = join(scratch, 'openapi.json')
  writeFileSync(schema, execFileSync(python, ['-c', dump], { cwd: backend, encoding: 'utf8' }))
  const output = check ? join(scratch, 'schema.d.ts') : target
  execFileSync('npx', ['openapi-typescript', schema, '-o', output], { cwd: root, stdio: 'inherit' })
  if (check && readFileSync(output, 'utf8') !== readFileSync(target, 'utf8')) {
    console.error('src/api/schema.d.ts is out of date: run `npm run gen:api`')
    process.exitCode = 1
  }
} finally {
  rmSync(scratch, { recursive: true, force: true })
}
