"""nb11 — растровые формулы (9.7)/(9.11): OCR и сверка с текстовым слоем.

Формулы (9.7) и (9.11) СП 22.13330.2016 в PDF — это встроенные растровые картинки
низкого разрешения (src 292x86 и 297x81 px), а не текстовый слой. Детерминированный
реконструктор (`text_layer_latex`) их не видит, поэтому здесь они распознаются OCR
(pix2text) и сверяются с текстовым слоем (обозначения «где …») и с частными случаями
(9.8)/(9.12) = K = tg²(45° ∓ φ/2), которые в текстовом слое есть.

Запуск из корня репо:
    .venv/bin/python ml/research/nb11_raster_formula_ocr.py
"""

from __future__ import annotations

import importlib
import importlib.util
import re
import sys
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PDF = REPO / "docs" / "normative-base" / "СП 22.13330.2016.pdf"
CROPS_DIR = REPO / "ml" / "research" / "crops"

import pdfplumber  # noqa: E402

TARGETS = {
    "9.7": (162, 9.22),
    "9.11": (163, 9.23),
}


_ocr = None


def _import_latex_ocr():
    global _ocr
    if _ocr is not None:
        return _ocr
    spec = importlib.util.find_spec("pix2text")
    pkg = types.ModuleType("pix2text")
    pkg.__path__ = list(spec.submodule_search_locations)
    pkg.__package__ = "pix2text"
    sys.modules["pix2text"] = pkg
    importlib.import_module("pix2text.consts")
    importlib.import_module("pix2text.utils")
    importlib.import_module("pix2text.latex_ocr")
    _ocr = sys.modules["pix2text.latex_ocr"].LatexOCR
    return _ocr


def number_bbox(page, number: str) -> tuple[float, float, float, float] | None:
    """BBox правого маркер-номера «(N)» на странице (по символам текстового слоя)."""
    glyphs = [c for c in page.chars if c["text"] in tuple(number) + ("(", ")")]
    for i, c in enumerate(glyphs):
        if c["text"] == "(":
            rest = "".join(g["text"] for g in glyphs[i : i + len(number) + 2])
            if rest == f"({number})":
                seg = glyphs[i : i + len(number) + 2]
                return (
                    min(g["x0"] for g in seg),
                    min(g["top"] for g in seg),
                    max(g["x1"] for g in seg),
                    max(g["bottom"] for g in seg),
                )
    return None


def raster_bbox(page, number: str) -> tuple[float, float, float, float] | None:
    """BBox встроенной картинки-формулы: ближайшая по вертикали к маркер-номеру (N)."""
    if not page.images:
        return None
    mk = number_bbox(page, number)
    if mk is None:
        return None
    mk_mid_y = (mk[1] + mk[3]) / 2
    im = min(page.images, key=lambda i: abs((i["top"] + i["bottom"]) / 2 - mk_mid_y))
    return im["x0"], im["top"], im["x1"], im["bottom"]


def render_crop(page, bbox, dpi: int = 400) -> Path:
    x0, top, x1, bottom = bbox
    pad = 8
    cropped = page.crop((x0 - pad, top - pad, x1 + pad, bottom + pad))
    return cropped.to_image(resolution=dpi).original


def ocr_latex(png_path: Path) -> str:
    from PIL import Image

    ocr = _import_latex_ocr()(device="cpu")
    return ocr.recognize(Image.open(png_path))["text"]


# Каноничный LaTeX (человеком сверен) для каждой формулы.
CLEAN_LATEX = {
    "9.7": (
        r"K_a = \frac{\cos^2(\varphi - \theta)}"
        r"{\cos^2 \theta \left[ 1 + "
        r"\sqrt{\frac{\sin(\delta + \varphi)\sin(\varphi - \beta)}"
        r"{\cos(\delta + \theta)\cos(\theta - \beta)}} \right]^2}"
    ),
    "9.11": (
        r"K_p = \frac{\cos^2(\varphi + \theta)}"
        r"{\cos^2 \theta \left[ 1 - "
        r"\sqrt{\frac{\sin(\varphi + \delta)\sin(\varphi + \beta)}"
        r"{\cos(\delta - \theta)\cos(\beta - \theta)}} \right]^2}"
    ),
}

# Expression (RHS) в явном виде по таблице символов, как в formulas.toml.
EXPRESSION = {
    "9.7": (
        "cos(phi - theta)**2 / (cos(theta)**2 * "
        "(1 + sqrt(sin(delta + phi)*sin(phi - beta) / "
        "(cos(delta + theta)*cos(theta - beta))))**2)"
    ),
    "9.11": (
        "cos(phi + theta)**2 / (cos(theta)**2 * "
        "(1 - sqrt(sin(phi + delta)*sin(phi + beta) / "
        "(cos(delta - theta)*cos(beta - theta))))**2)"
    ),
}


def notation_text(pages: list[str], page_no: int) -> str:
    """Строки «где …» на странице (обозначения формулы), из текстового слоя."""
    lines = pages[page_no - 1].splitlines() if pages else []
    out = []
    grabbing = False
    for line in lines:
        if re.search(r"где\s", line):
            grabbing = True
        if grabbing:
            out.append(line)
        if grabbing and (line.strip().endswith((".")) or re.match(r"^9\.", line.strip())):
            break
    return "\n".join(out)


def _rhs(latex: str):
    from latex2sympy2 import latex2sympy

    rhs_str = latex.split("=", 1)[1].strip()
    return latex2sympy(rhs_str)


def reduce_to_special(expression: str, sign: str) -> None:
    """Численная проверка: общий случай при β=θ=δ=0 совпадает с частным (9.8)/(9.12)."""
    from sympy import pi, symbols, sympify, tan

    phi, beta, theta, delta = symbols("phi beta theta delta")
    local = {"phi": phi, "beta": beta, "theta": theta, "delta": delta}
    general = sympify(expression, locals=local)
    special = tan(pi / 4 + sign * phi / 2) ** 2
    for val in (0.3, 0.6, 1.0):
        g = general.subs({phi: val, beta: 0, theta: 0, delta: 0}).evalf()
        s = special.subs(phi, val).evalf()
        ok = abs(g - s) < 1e-12
        print(f"  φ={val}: общий={float(g):.12f}  частный={float(s):.12f}  |Δ|={float(abs(g - s)):.1e}  {'OK' if ok else 'FAIL'}")
    return None


def main() -> int:
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    pages_text = []
    with pdfplumber.open(PDF) as doc:
        pages_text = [p.extract_text() or "" for p in doc.pages]
        for number, (page_no, clause) in TARGETS.items():
            page = doc.pages[page_no - 1]
            nb = number_bbox(page, number)
            rb = raster_bbox(page, number)
            im = next((i for i in page.images if abs(i["top"] - rb[1]) < 0.1), page.images[0] if page.images else {})
            print(f"==== ({number}) p{page_no} (пункт {clause}) ====")
            print(f"  растр src={im.get('srcsize')} bbox={rb}")
            print(f"  маркер-номер bbox={nb}")
            region = rb
            png = CROPS_DIR / f"nb11_{number.replace('.', '_')}.png"
            render_crop(page, region).save(png)
            print(f"  кроп -> {png.relative_to(REPO)}")
            latex = ocr_latex(png)
            print(f"  OCR   : {latex}")
            print(f"  CLEAN : {CLEAN_LATEX[number]}")
            print(f"  expr  : {EXPRESSION[number]}")
            print(f"  обозначения:\n{notation_text(pages_text, page_no)}")
            sign = -1 if clause == 9.22 else 1
            print(f"  редукция к частному (β=θ=δ=0) tg²(45°{'−' if sign < 0 else '+'}φ/2):")
            reduce_to_special(EXPRESSION[number], sign)
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
