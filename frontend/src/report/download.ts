const FILENAME = /filename\*?=(?:UTF-8'')?"?([^";]+)"?/i

export function fileNameFrom(disposition: string | null, fallback: string): string {
  const match = disposition ? FILENAME.exec(disposition) : null
  return match ? decodeURIComponent(match[1].trim()) : fallback
}

export function saveFile(blob: Blob, name: string): void {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = name
  document.body.append(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}
