import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { jumpTo } from './jumpTo'

const scrollIntoView = vi.fn()

function page() {
  render(
    <>
      <a href="#target" onClick={(event) => jumpTo(event, 'target')}>
        to target
      </a>
      <a href="#missing" onClick={(event) => jumpTo(event, 'missing')}>
        to nowhere
      </a>
      <h2 id="target" tabIndex={-1}>
        Target
      </h2>
    </>,
  )
}

beforeEach(() => {
  Element.prototype.scrollIntoView = scrollIntoView
})

afterEach(() => {
  scrollIntoView.mockReset()
  delete (Element.prototype as Partial<Element>).scrollIntoView
})

describe('jumpTo', () => {
  it('scrolls to the target and moves focus to it without a history entry', () => {
    page()
    const link = screen.getByRole('link', { name: 'to target' })

    const followed = fireEvent.click(link)

    expect(followed).toBe(false)
    expect(scrollIntoView).toHaveBeenCalledWith({ block: 'start' })
    expect(screen.getByRole('heading', { name: 'Target' })).toHaveFocus()
  })

  it.each([{ ctrlKey: true }, { metaKey: true }, { shiftKey: true }, { altKey: true }, { button: 1 }])(
    'leaves a modified click %o to the browser',
    (init) => {
      page()

      const followed = fireEvent.click(screen.getByRole('link', { name: 'to target' }), init)

      expect(followed).toBe(true)
      expect(scrollIntoView).not.toHaveBeenCalled()
    },
  )

  it('leaves the link to the browser when the target is missing', () => {
    page()

    const followed = fireEvent.click(screen.getByRole('link', { name: 'to nowhere' }))

    expect(followed).toBe(true)
    expect(scrollIntoView).not.toHaveBeenCalled()
  })
})
