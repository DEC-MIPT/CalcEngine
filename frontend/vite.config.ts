/// <reference types="vitest/config" />
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { rmSync } from 'node:fs'
import { createRequire } from 'node:module'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig, type Plugin } from 'vite'

const mathjaxVersion = (createRequire(import.meta.url)('mathjax-full/package.json') as { version: string }).version

const MOCK_WORKER = 'mockServiceWorker.js'

function dropMockWorker(): Plugin {
  let outDir = ''
  let mock = false
  return {
    name: 'drop-mock-worker',
    apply: 'build',
    configResolved(config) {
      outDir = resolve(config.root, config.build.outDir)
      mock = config.mode === 'mock'
    },
    closeBundle() {
      if (!mock) rmSync(resolve(outDir, MOCK_WORKER), { force: true })
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), dropMockWorker()],
  define: { PACKAGE_VERSION: JSON.stringify(mathjaxVersion) },
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    exclude: ['e2e/**', 'node_modules/**'],
    coverage: {
      provider: 'v8',
      thresholds: {
        branches: 95,
      },
    },
  },
})
