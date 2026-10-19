import { describe, expect, it } from 'vitest'
import { mapReportErrors } from './errors'

const keys = ['title.designation', 'developer.date', 'signature_block']

describe('mapReportErrors (design.md decision 7)', () => {
  it('maps the path after body to a report field and keeps the first message of a field', () => {
    expect(
      mapReportErrors(
        [
          { location: ['body', 'title', 'designation'], message: 'too long' },
          { location: ['body', 'title', 'designation'], message: 'second' },
          { location: ['body', 'developer', 'date'], message: 'bad date' },
          { location: ['body', 'signature_block'], message: 'not a boolean' },
        ],
        keys,
      ),
    ).toEqual({
      byField: { 'title.designation': 'too long', 'developer.date': 'bad date', signature_block: 'not a boolean' },
      general: [],
    })
  })

  it('keeps an entry that names no field, or names it outside the body, for the top of the form', () => {
    expect(
      mapReportErrors(
        [
          { location: ['body'], message: 'the signature block needs the surname and the date of developer' },
          { location: ['path', 'result_id'], message: 'bad id' },
          { location: ['body', 'title', 'unknown'], message: 'extra' },
        ],
        keys,
      ),
    ).toEqual({
      byField: {},
      general: ['the signature block needs the surname and the date of developer', 'bad id', 'extra'],
    })
  })
})
