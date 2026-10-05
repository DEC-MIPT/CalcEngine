import { browserAdaptor } from 'mathjax-full/js/adaptors/browserAdaptor.js'
import { RegisterHTMLHandler } from 'mathjax-full/js/handlers/html.js'
import { TeX } from 'mathjax-full/js/input/tex.js'
import 'mathjax-full/js/input/tex/ams/AmsConfiguration.js'
import 'mathjax-full/js/input/tex/base/BaseConfiguration.js'
import { mathjax } from 'mathjax-full/js/mathjax.js'
import { SVG } from 'mathjax-full/js/output/svg.js'

type Document = ReturnType<typeof createDocument>

function createDocument() {
  const adaptor = browserAdaptor()
  RegisterHTMLHandler(adaptor)
  return mathjax.document('', {
    InputJax: new TeX({
      packages: ['base', 'ams'],
      formatError: (_jax: unknown, error: Error): never => {
        throw error
      },
    }),
    OutputJax: new SVG({ fontCache: 'none' }),
  })
}

let document: Document | undefined

export function typeset(latex: string, display: boolean): Node | null {
  document ??= createDocument()
  try {
    return document.convert(latex, { display }) as Node
  } catch {
    return null
  }
}
