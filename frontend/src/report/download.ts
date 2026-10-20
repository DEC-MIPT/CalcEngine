const EXTENDED = /filename\*\s*=\s*UTF-8''([^;]+)/i
const PLAIN = /filename\s*=\s*"?([^";]+)"?/i
const REVOKE_DELAY_MS = 40_000

function decoded(value: string): string | null {
  try {
    return decodeURIComponent(value)
  } catch {
    return null
  }
}

export function fileNameFrom(disposition: string | null, fallback: string): string {
  if (!disposition) return fallback
  const extended = EXTENDED.exec(disposition)?.[1].trim()
  const plain = PLAIN.exec(disposition)?.[1].trim()
  return (extended && decoded(extended)) || plain || fallback
}

export function saveFile(blob: Blob, name: string): void {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = name
  document.body.append(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), REVOKE_DELAY_MS)
}
