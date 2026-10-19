import { afterEach, describe, expect, it, vi } from 'vitest'
import { fileNameFrom, saveFile } from './download'

afterEach(() => {
  vi.restoreAllMocks()
  Reflect.deleteProperty(URL, 'createObjectURL')
  Reflect.deleteProperty(URL, 'revokeObjectURL')
})

describe('fileNameFrom', () => {
  it.each([
    ['attachment; filename="dec-report-1.docx"', 'dec-report-1.docx'],
    ['attachment; filename=plain.docx', 'plain.docx'],
    ["attachment; filename*=UTF-8''%D0%BE%D1%82%D1%87%D1%91%D1%82.docx", 'отчёт.docx'],
    ['attachment; filename="100%.docx"', '100%.docx'],
    ["attachment; filename=\"plain.docx\"; filename*=UTF-8''%D0%BE.docx", 'о.docx'],
    ["attachment; filename=\"plain.docx\"; filename*=UTF-8''%E0%A4%A.docx", 'plain.docx'],
  ])('reads the name from %s', (header, name) => {
    expect(fileNameFrom(header, 'fallback.docx')).toBe(name)
  })

  it.each([null, 'attachment', "attachment; filename*=UTF-8''%E0%A4%A.docx"])('falls back when the header gives no name (%s)', (header) => {
    expect(fileNameFrom(header, 'fallback.docx')).toBe('fallback.docx')
  })
})

describe('saveFile', () => {
  it('clicks a temporary download link with the name and releases the object URL', () => {
    const create = vi.fn(() => 'blob:report')
    const revoke = vi.fn()
    Object.assign(URL, { createObjectURL: create, revokeObjectURL: revoke })
    const clicked: { href: string; download: string }[] = []
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) {
      clicked.push({ href: this.href, download: this.download })
    })

    vi.useFakeTimers()

    saveFile(new Blob(['x']), 'report.docx')

    expect(clicked).toEqual([{ href: 'blob:report', download: 'report.docx' }])
    expect(revoke).not.toHaveBeenCalled()
    vi.runAllTimers()
    vi.useRealTimers()
    expect(revoke).toHaveBeenCalledWith('blob:report')
    expect(document.querySelector('a[download]')).toBeNull()
  })
})
