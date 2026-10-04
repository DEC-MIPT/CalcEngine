r"""Полный обзор формул: сильная автоматика + HTML «PDF ↔ LaTeX» по одному СП за раз.

Для указанного PDF проходит все страницы, реконструирует формулы нашим детерминированным
слоем (`text_layer_latex.reconstruct_latex`) и для каждой считает:

* структурные дефекты (баланс скобок, наличие отношения, PUA-мусор, утечка прозы);
* разбор `latex2sympy` каскадом base → chem/flat → mul → E-обёртка, со сбросом
  глобального `var` и разворотом знаковых ветвей (как в nb08 §11);
* кириллицу: базовые буквы-двойники и русские слова в индексах;
* предложенную нормализацию кириллицы (визуальная латиница в базе + ``\text{}`` в индексах).

Пишет HTML (кроп из PDF + MathJax + статусы) и JSON-сводку. Никаких моделей/LLM, без
хардкода под документ: страницы и формулы находятся автоматически. Прод не трогается.

Запуск:

    python research/verify_corpus.py "../docs/normative-base/СП 31.13330.2021.pdf" \
        --out research/human-views/sp31.html --json research/human-views/sp31.json

С ``--include-missed`` в HTML добавляется секция «Не извлечено» — маркеры ``(N)``, из
которых не собралась формула (нет отношения / не собрано), с кропом и строкой контекста:
нужно, чтобы глазами отделить пропущенную формулу от прозаической ссылки.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

import latex2sympy2
import pdfplumber
import pymupdf

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

from text_layer_latex import (  # noqa: E402
    _marker,
    mathtt_E,
    reconstruct_latex,
    sign_variants,
    split_juxtaposed,
    to_parseable,
)
from normatives_pipeline.formulas.validation import latex2sympy  # noqa: E402

NUM_RE = re.compile(r"\((\d{1,2}(?:\.\d+)?)\)")
# Отношение: символьные и командные формы. Реконструктор выдаёт ``\leq``/``\geq``
# из карты Symbol-шрифта (text_layer_latex ``_REL``/``_PUA``), поэтому одной ``[=≥≤≠]``
# мало — иначе формулы с ``<``/``>``/``\leq``/``\geq``/``\neq`` отбрасываются (nb08 §11.3).
REL_RE = re.compile(r"[=≥≤≠<>]|\\leq|\\geq|\\neq|\\approx|\\lt|\\gt|\\ll|\\gg")
CYR_RE = re.compile(r"[А-Яа-яЁё]")
PUA_RE = re.compile(r"[\ue000-\uf8ff\uf0e0-\uf0ff]")
TEXT_GROUP_RE = re.compile(r"([_^])\{([^}]*)\}")

# Буквы кириллицы, визуально тождественные латинским (базовый уровень формулы).
VISUAL = str.maketrans(
    "АВЕКМНОРСТУХаеорсху", "ABEKMHOPCTYXaeopcxy"
)

_FAIL = (Exception,)


def structural_issues(latex: str) -> list[str]:
    issues = []
    plain = latex.replace(r"\{", "").replace(r"\}", "")
    if plain.count("{") != plain.count("}"):
        issues.append("скобки")
    if not REL_RE.search(latex):
        issues.append("нет отношения")
    if PUA_RE.search(latex):
        issues.append("PUA-мусор")
    base = TEXT_GROUP_RE.sub("", plain)
    if re.search(r"[А-Яа-яЁё]{3,}", base):
        issues.append("проза в базе")
    return issues


def _reset() -> None:
    """Сбрасывает глобальный ``var`` latex2sympy2 (утечка состояния между вызовами).

    ``latex2sympy2.convert_atom`` объявляет ``global var`` и на ветке дифференциала
    присваивает ему ``Symbol``; без сброса следующая формула падает. См. nb08 §10.2.
    """
    latex2sympy2.var = {}
    latex2sympy2.variances = {}


def _parses(parseable: str) -> bool:
    _reset()
    try:
        latex2sympy(parseable)
        return True
    except _FAIL:
        return False


def _chem(s: str) -> str:
    return re.sub(r"([A-Z][a-z]?)\^\{?\d*[+-]\}?", r"\1", s)


def _flat(s: str) -> str:
    return re.sub(r"_\{([A-Za-z0-9]+)\}", r"\1", s)


def _variants(display: str) -> list[str]:
    """Каскад трансформаций разбора (nb08 §11): base → chem/flat → mul → E-обёртка."""
    b = to_parseable(display).strip().rstrip(",;.").strip()
    if not b:
        return []
    return [
        b,
        _chem(b),
        _flat(b),
        _chem(_flat(b)),
        split_juxtaposed(b),
        mathtt_E(b),
        mathtt_E(split_juxtaposed(b)),
        mathtt_E(split_juxtaposed(_flat(b))),
    ]


def _parses_formula(expr: str) -> bool:
    """Формула засчитана, если хоть один вариант каскада парсится во всех знаковых ветвях."""
    for v in _variants(expr):
        branches = sign_variants(v)
        if branches and all(_parses(x) for x in branches):
            return True
    return False


def parse_status(latex: str) -> str:
    """Системы разбираем построчно; одиночную формулу — каскадом (nb08 §11)."""
    if r"\begin{aligned}" in latex:
        body = latex.split(r"\begin{aligned}", 1)[1].split(r"\end{aligned}", 1)[0]
        equations = [e.strip() for e in body.split(r"\\") if e.strip()]
        return "ok" if equations and all(_parses_formula(e) for e in equations) else "err"
    return "ok" if _parses_formula(latex) else "err"


def normalize_cyrillic(latex: str) -> str:
    """Базовая кириллица-двойник → латиница; русские слова в индексах → ``\\text{}``."""
    out = []
    pos = 0
    for m in TEXT_GROUP_RE.finditer(latex):
        out.append(latex[pos:m.start()].translate(VISUAL))
        group = m.group(2)
        if CYR_RE.search(group) and len(CYR_RE.findall(group)) >= 2:
            out.append(f"{m.group(1)}\\text{{{group}}}")
        else:
            out.append(f"{m.group(1)}{{{group.translate(VISUAL)}}}")
        pos = m.end()
    out.append(latex[pos:].translate(VISUAL))
    return "".join(out)


def _crop(doc: pymupdf.Document, page_no: int, y0: float, y1: float, out_png: Path) -> bool:
    pg = doc[page_no - 1]
    W = pg.rect.width
    rect = pymupdf.Rect(0.04 * W, y0 - 6, 0.99 * W, y1 + 6)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    pg.get_pixmap(clip=rect, dpi=200).save(out_png)
    return True


def _marker_anywhere(chars: list[dict], number: str) -> tuple[float, float] | None:
    """Маркер ``(N)`` в любом месте строки, не только в правом поле (для прозы/ссылок)."""
    seq = f"({number})"
    texts = [c["text"] for c in chars]
    for i in range(len(texts) - len(seq) + 1):
        if "".join(texts[i : i + len(seq)]) == seq:
            return chars[i]["top"], chars[i]["x0"]
    return None


def _card(rec: dict, png_rel: str) -> str:
    badges = "".join(
        f'<span class="b {"bad" if i in ("скобки", "нет отношения", "PUA-мусор", "проза в базе") else "warn"}">{html.escape(i)}</span>'
        for i in (rec["issues"] or ["структурно ok"])
    )
    cls = "err" if rec["parse"] == "err" else "ok"
    norm = ""
    if rec["normalized"] != rec["latex"]:
        norm = (
            "<h4>предложенная нормализация кириллицы</h4>"
            f'<pre>{html.escape(rec["normalized"])}</pre>'
            f'<div class="math">\\[{html.escape(rec["normalized"])}\\]</div>'
        )
    return f"""<section class="card">
 <div class="left"><img src="{html.escape(png_rel)}" alt="pdf crop">
   <figcaption>стр. {rec['page']}, ({html.escape(rec['number'])})</figcaption></div>
 <div class="right">
   <div class="hd"><b>({html.escape(rec['number'])})</b> стр. {rec['page']}
     <label class="ok"><input type="checkbox" class="okbox" data-id="{rec['page']}:{html.escape(rec['number'])}"> OK</label>
     <span class="b {cls}">sympy: {rec['parse']}</span> {badges}</div>
   <h4>LaTeX (текущий)</h4><pre>{html.escape(rec['latex'])}</pre>
   <div class="math">\\[{html.escape(rec['latex'])}\\]</div>
    {norm}
 </div></section>"""


def _missed_card(rec: dict, png_rel: str) -> str:
    return f"""<section class="card miss">
 <div class="left"><img src="{html.escape(png_rel)}" alt="pdf crop">
   <figcaption>стр. {rec['page']}, ({html.escape(rec['number'])})</figcaption></div>
 <div class="right">
   <div class="hd"><b>({html.escape(rec['number'])})</b> стр. {rec['page']}
     <label class="ok"><input type="checkbox" class="okbox" data-id="{rec['page']}:{html.escape(rec['number'])}"> OK</label>
     <span class="b bad">не извлечено: {html.escape(rec['reason'])}</span></div>
   <h4>строка, где найден номер</h4><pre>{html.escape(rec.get('context', ''))}</pre>
   <h4>LaTeX (частично)</h4><pre>{html.escape(rec['latex'] or '—')}</pre>
 </div></section>"""


def build(pdf: Path, out_html: Path, out_json: Path, limit: int | None,
          include_missed: bool = False) -> dict:
    assets = out_html.parent / (out_html.stem + "_assets")
    records, missed = [], []
    with pymupdf.open(str(pdf)) as mdoc, pdfplumber.open(str(pdf)) as doc:
        for page_no, page in enumerate(doc.pages, start=1):
            raw = "".join(c["text"] for c in page.chars)
            page_text = None
            for number in sorted(set(NUM_RE.findall(raw))):
                if limit and len(records) >= limit:
                    break
                latex = reconstruct_latex(page, number)
                accepted = bool(latex and REL_RE.search(latex))
                if not accepted and not include_missed:
                    continue
                marker = _marker(page.chars, number) or _marker_anywhere(page.chars, number)
                png = assets / f"p{page_no}_n{number.replace('.', '_')}.png"
                rec = {
                    "page": page_no,
                    "number": number,
                    "latex": latex or "",
                    "normalized": normalize_cyrillic(latex or ""),
                    "issues": structural_issues(latex) if latex else [],
                    "parse": parse_status(latex) if latex else "—",
                    "cyrillic_base": bool(latex and CYR_RE.search(TEXT_GROUP_RE.sub("", latex))),
                    "missed": not accepted,
                    "reason": "" if accepted else ("нет отношения" if latex else "не собрано"),
                }
                if not accepted:
                    if page_text is None:
                        page_text = page.extract_text() or ""
                    rec["context"] = next(
                        (ln.strip() for ln in page_text.splitlines() if f"({number})" in ln), "")
                if marker:
                    near = [c for c in page.chars if c["text"].strip()
                            and c["x0"] < marker[1] and abs(c["top"] - marker[0]) < 45]
                    y0 = min([c["top"] for c in near] + [marker[0]])
                    y1 = max([c["bottom"] for c in near] + [marker[0]])
                    if _crop(mdoc, page_no, y0, y1, png):
                        rec["png"] = png.relative_to(out_html.parent).as_posix()
                (records if accepted else missed).append(rec)
            if limit and len(records) >= limit:
                break

    cards = "".join(_card(r, r["png"]) for r in records if "png" in r)
    missed_cards = "".join(_missed_card(r, r["png"]) for r in missed if "png" in r)
    summary = {
        "pdf": pdf.name,
        "formulas": len(records),
        "sympy_ok": sum(r["parse"] == "ok" for r in records),
        "structural_ok": sum(not r["issues"] for r in records),
        "cyrillic_base": sum(r["cyrillic_base"] for r in records),
        "changed_by_normalization": sum(r["normalized"] != r["latex"] for r in records),
        "missed": len(missed),
        "issues": {k: sum(k in r["issues"] for r in records) for k in
                   ("скобки", "нет отношения", "PUA-мусор", "проза в базе")},
    }
    toolbar = (
        '<div id="bar"><span id="count"></span>'
        f'<button id="dl" data-name="{out_html.stem}_checks.json">Скачать отметки (JSON)</button>'
        '<button id="reset">Сбросить</button>'
        '<span class="hint">Отметьте «OK», где всё верно; где галочки нет — улучшаем. '
        'Скачанный файл положите в <code>ml/research/human-views/</code>.</span></div>'
    )
    script = """<script>
const KEY = "checks::" + document.title;
const boxes = Array.from(document.querySelectorAll('input.okbox'));
function load(){ try{ const s = JSON.parse(localStorage.getItem(KEY) || '{}');
  boxes.forEach(b => { if (s[b.dataset.id]) b.checked = true; }); }catch(e){} }
function save(){ const s = {}; boxes.forEach(b => { if (b.checked) s[b.dataset.id] = 1; });
  localStorage.setItem(KEY, JSON.stringify(s)); }
function upd(){ const ok = boxes.filter(b => b.checked).length;
  document.getElementById('count').textContent =
    'OK: ' + ok + ' / ' + boxes.length + ' (без отметки: ' + (boxes.length - ok) + ')'; }
boxes.forEach(b => b.addEventListener('change', () => { save(); upd(); }));
document.getElementById('reset').addEventListener('click', () => {
  if (!confirm('Сбросить все отметки?')) return;
  localStorage.removeItem(KEY); boxes.forEach(b => b.checked = false); upd(); });
document.getElementById('dl').addEventListener('click', () => {
  const ok = boxes.filter(b => b.checked).map(b => b.dataset.id);
  const data = {file: document.title, total: boxes.length, ok: ok,
    not_ok: boxes.filter(b => !b.checked).map(b => b.dataset.id)};
  const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = document.getElementById('dl').dataset.name; a.click(); URL.revokeObjectURL(a.href); });
load(); upd();
</script>"""
    page = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Обзор формул — {html.escape(pdf.name)}</title>
<script>window.MathJax={{tex:{{displayMath:[['\\\\[','\\\\]']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
 body{{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:20px;color:#1b1f23}}
 .card{{display:grid;grid-template-columns:1.1fr 1fr;gap:16px;border:1px solid #d0d7de;
   border-radius:8px;padding:12px;margin:12px 0;background:#fff}}
 .left img{{max-width:100%;border:1px solid #ccc;border-radius:4px}}
 figcaption{{font-size:12px;color:#666}}
 pre{{background:#f6f8fa;border:1px solid #e1e4e8;border-radius:6px;padding:8px;
   overflow:auto;font-size:12px;white-space:pre-wrap}}
 .math{{font-size:17px;overflow-x:auto}}
 .b{{display:inline-block;border-radius:10px;padding:1px 8px;font-size:12px;margin-left:4px}}
 .b.ok{{background:#dafbe1;color:#116329}} .b.err{{background:#ffebe9;color:#a40e26}}
 .b.warn{{background:#fff8c5;color:#7d4e00}} .b.bad{{background:#ffebe9;color:#a40e26}}
 .hd{{font-size:14px;margin-bottom:6px}}
 .card.miss{{border-color:#f0b8b8;background:#fff8f8}}
 h2{{margin-top:28px}}
 #bar{{position:sticky;top:0;background:#fff;border-bottom:1px solid #d0d7de;
   padding:8px 0;z-index:10;margin:-20px 0 12px}}
 #bar button{{margin-left:8px;padding:4px 10px;border:1px solid #bbb;border-radius:6px;
   background:#f6f8fa;cursor:pointer}}
 .hint{{color:#666;font-size:12px;margin-left:8px}}
 label.ok{{font-weight:normal;margin-left:8px;white-space:nowrap}}
</style></head><body>
<h1>Обзор формул — {html.escape(pdf.name)}</h1>
<p>формул {summary['formulas']} · sympy ok {summary['sympy_ok']} ·
 структурно ok {summary['structural_ok']} · с кириллицей в базе {summary['cyrillic_base']} ·
 меняет нормализация {summary['changed_by_normalization']} ·
 <b>не извлечено {summary['missed']}</b></p>
{toolbar}
<h2>Извлечённые формулы ({len(records)})</h2>
{cards}
{f'<h2>Не извлечено / требует проверки ({len(missed)})</h2>' if missed else ''}
{missed_cards}
{script}</body></html>"""
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding="utf-8")
    out_json.write_text(
        json.dumps({"summary": summary, "records": records, "missed": missed},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--include-missed", action="store_true",
                    help="включить в HTML маркеры (N), не собранные в формулу (для проверки полноты)")
    args = ap.parse_args()
    out_json = args.json or args.out.with_suffix(".json")
    summary = build(args.pdf, args.out, out_json, args.limit, args.include_missed)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("HTML:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
