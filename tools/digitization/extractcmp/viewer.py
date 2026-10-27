"""Лист порции в HTML: вырезка страницы PDF рядом с выписками и записью черновика."""

import base64
import html
import re
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from extractcmp.checkpoints import ControlPoint
from extractcmp.portions import Item

PAGE_WIDTH = 1240
"""Ширина страницы в пикселях при 150 dpi: в этих координатах B записывает области."""
PAGE_HEIGHT = 1755
"""Высота страницы в пикселях при 150 dpi."""
DPI = 150
PAD = 40
"""Поля полосы над и под областью, пиксели."""
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"

Renderer = Callable[[int, int, int], bytes]
"""Отрисовка полосы страницы: (страница, верх, высота) → PNG."""

_PAGE = re.compile(r"стр\.\s*(\d+)")
_X = re.compile(r"x\s*(\d+)\s*-\s*(\d+)")
_Y = re.compile(r"y\s*(\d+)\s*-\s*(\d+)")


@dataclass(frozen=True)
class Crop:
    """Полоса страницы во всю ширину и рамка области на ней.

    Attributes:
        page: номер страницы PDF, с единицы.
        top: верх полосы, пиксели.
        height: высота полосы, пиксели.
        box: рамка области ``(x0, y0, x1, y1)`` в координатах страницы.
    """

    page: int
    top: int
    height: int
    box: tuple[int, int, int, int]


def pages_of(page: str) -> list[int]:
    """Разбирает поле ``page`` проверки.

    Args:
        page: например ``36`` или ``37, 38``; ``—``, если страницы нет.

    Returns:
        Номера страниц.
    """
    return [int(p) for p in re.findall(r"\d+", page)]


def crops(region: str, pages: Sequence[int]) -> list[Crop]:
    """Находит полосы страниц по описанию области из B.

    Текст до первого «стр. N» относится к первой странице проверки, текст после «стр. N» —
    к странице N. Каждый диапазон ``y a-b`` даёт полосу; диапазон ``x a-b`` того же куска
    задаёт рамку, иначе рамка во всю ширину. Страница без диапазонов показывается целиком.

    Args:
        region: область страницы по B.
        pages: страницы проверки.

    Returns:
        Полосы в порядке текста.
    """
    if not pages:
        return []
    parts: list[tuple[int, str]] = []
    marks = list(_PAGE.finditer(region))
    head = region[: marks[0].start()] if marks else region
    parts.append((pages[0], head))
    for number, mark in enumerate(marks):
        end = marks[number + 1].start() if number + 1 < len(marks) else len(region)
        parts.append((int(mark.group(1)), region[mark.end():end]))
    found: list[Crop] = []
    seen: set[int] = set()
    for page, text in parts:
        x = _X.search(text)
        x0, x1 = (int(x.group(1)), int(x.group(2))) if x else (0, PAGE_WIDTH)
        for y in _Y.finditer(text):
            y0, y1 = int(y.group(1)), int(y.group(2))
            top = max(0, y0 - PAD)
            found.append(Crop(page, top, min(PAGE_HEIGHT, y1 + PAD) - top, (x0, y0, x1, y1)))
            seen.add(page)
    named = [page for page, text in parts[1:] if page not in seen]
    whole = named if found else [*named, *(p for p in pages if p not in named)]
    found += [Crop(p, 0, PAGE_HEIGHT, (0, 0, PAGE_WIDTH, PAGE_HEIGHT)) for p in dict.fromkeys(whole)]
    return found


def pdftoppm(pdf: Path) -> Renderer:
    """Отрисовывает полосы страниц программой ``pdftoppm`` (poppler).

    Args:
        pdf: файл нормы.

    Returns:
        Функция отрисовки.
    """

    def render(page: int, top: int, height: int) -> bytes:
        args = ["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page), "-x", "0", "-y", str(top),
                "-W", str(PAGE_WIDTH), "-H", str(height), "-png", str(pdf)]
        return subprocess.run(args, capture_output=True, check=True).stdout

    return render


def _number(value: object) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def evaluate(tree: Mapping[str, Any], values: Mapping[str, Any]) -> float | None:
    """Вычисляет дерево выражения черновика.

    Args:
        tree: дерево в формате файла типа.
        values: значения символов: числа или числа, записанные строкой (как в методичке).

    Returns:
        Значение; ``None``, если символ не задан числом или узел незнаком.
    """
    kind = tree["kind"]
    if kind == "number":
        return float(tree["value"])
    if kind == "symbol":
        return _number(values.get(tree["name"]))
    if kind == "neg":
        inner = evaluate(tree["operand"], values)
        return None if inner is None else -inner
    ops = {"add": float.__add__, "sub": float.__sub__, "mul": float.__mul__, "div": float.__truediv__}
    if kind not in ops:
        return None
    left, right = evaluate(tree["left"], values), evaluate(tree["right"], values)
    if left is None or right is None or (kind == "div" and right == 0):
        return None
    return ops[kind](left, right)


def infix(tree: Mapping[str, Any]) -> str:
    """Записывает дерево выражения строкой со скобками.

    Args:
        tree: дерево в формате файла типа.
    """
    kind = tree["kind"]
    if kind == "number":
        return f"{tree['value']:g}"
    if kind == "symbol":
        return str(tree["name"])
    if kind == "neg":
        return f"−{infix(tree['operand'])}"
    signs = {"add": "+", "sub": "−", "mul": "·", "div": "/"}
    if kind not in signs:
        return f"<{kind}>"
    return f"({infix(tree['left'])} {signs[kind]} {infix(tree['right'])})"


@dataclass(frozen=True)
class Context:
    """Данные, общие для всех проверок листа.

    Attributes:
        draft: черновик файла типа.
        records: локальный id проверки → ключи записей черновика из сопоставления.
        mapping: сопоставление записей черновика с проверками.
        points: контрольные точки по id.
        render: отрисовка полос страниц.
    """

    draft: Mapping[str, Any]
    records: Mapping[str, Sequence[str]]
    mapping: Mapping[str, Any]
    points: Mapping[str, ControlPoint]
    render: Renderer


def context(draft: Mapping[str, Any], mapping: Mapping[str, Any], points: Sequence[ControlPoint],
            render: Renderer) -> Context:
    """Собирает данные для страниц листов.

    Args:
        draft: черновик файла типа.
        mapping: сопоставление записей черновика с проверками.
        points: контрольные точки.
        render: отрисовка полос страниц.
    """
    records: dict[str, list[str]] = {}
    for key, where in mapping.items():
        for local in where["items"]:
            records.setdefault(local, []).append(key)
    return Context(draft, records, mapping, {p.cp_id: p for p in points}, render)


def _e(value: object) -> str:
    return html.escape(str(value))


def _record(ctx: Context, key: str) -> dict[str, Any]:
    where = ctx.mapping[key]
    return ctx.draft[where["list"]][where["index"]]


def _crop_html(ctx: Context, crop: Crop) -> str:
    png = base64.b64encode(ctx.render(crop.page, crop.top, crop.height)).decode("ascii")
    x0, y0, x1, y1 = crop.box
    box = (f"left:{100 * x0 / PAGE_WIDTH:.2f}%;width:{100 * (x1 - x0) / PAGE_WIDTH:.2f}%;"
           f"top:{100 * (y0 - crop.top) / crop.height:.2f}%;height:{100 * (y1 - y0) / crop.height:.2f}%")
    whole = crop.height == PAGE_HEIGHT
    return (f'<figure class="crop{" whole" if whole else ""}"><div class="frame">'
            f'<img alt="Страница {crop.page}" src="data:image/png;base64,{png}">'
            + ("" if whole else f'<span class="box" style="{box}"></span>')
            + f"</div><figcaption>стр. {crop.page}" + (" целиком" if whole else f", y {y0}–{y1}")
            + "</figcaption></figure>")


def _units(units: Mapping[str, str]) -> str:
    return ", ".join(f"{_e(k)}: {_e(v)}" for k, v in units.items())


def _record_html(ctx: Context, key: str) -> str:
    rec = _record(ctx, key)
    rows: list[tuple[str, str]] = []
    if rec.get("latex"):
        rows.append(("LaTeX", f'<span class="tex" data-tex="{_e(rec["latex"])}">{_e(rec["latex"])}</span>'
                              f'<code class="raw">{_e(rec["latex"])}</code>'))
    if rec.get("tree"):
        rows.append(("дерево", f"<code>{_e(infix(rec['tree']))}</code>"))
    if "value" in rec:
        heading = (f"; {_e(rec['heading_symbol'])} = {rec['heading_value']:g} {_e(rec['heading_unit'])}"
                   if rec.get("heading_value") is not None else "")
        rows.append(("значение", f"{_e(rec.get('symbol', rec.get('parameter')))} = {_e(rec['value'])}"
                                 f" [{_e(rec.get('unit'))}]{heading}"))
    if rec.get("units"):
        rows.append(("единицы", _units(rec["units"])))
    refs = "; ".join(f"{_e(r['document'])}, {_e(r['edition'])}, {_e(r['clause'])} ({_e(r['status'])})"
                     for r in rec.get("norm_refs", []))
    rows.append(("ссылка", refs or "—"))
    rows.append(("страница", _e(rec.get("page", "—"))))
    rows.append(("статус", _e(rec.get("verification", {}).get("status", "—"))))
    body = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    return f'<div class="record"><h4>Запись каталога <code>{_e(key)}</code></h4><table>{body}</table></div>'


def _point_html(ctx: Context, point: ControlPoint) -> str:
    lines = []
    for target in point.target:
        for key in ctx.records.get(target, []):
            rec = _record(ctx, key)
            if rec.get("tree") is None:
                continue
            value = evaluate(rec["tree"], point.inputs)
            if value is not None:
                lines.append(f'<p class="calc"><b>По дереву черновика</b> <code>{_e(key)}</code>: '
                             f"{_e(rec.get('result_symbol', key))} = {value:.10g} "
                             "(вычислено кодом; не значение нормы и не вердикт)</p>")
    return "".join(lines)


def _verdict(entry: Mapping[str, Any]) -> str:
    if not entry.get("verdict"):
        return '<p class="verdict empty">Вердикта нет</p>'
    parts = [f"<b>{_e(entry['verdict'])}</b>", _e(entry.get("by") or ""), _e(entry.get("at") or "")]
    if entry.get("corrected"):
        parts.append(f"исправление: <code>{_e(entry['corrected'])}</code>")
    if entry.get("comment"):
        parts.append(_e(entry["comment"]))
    return '<p class="verdict">' + " · ".join(p for p in parts if p) + "</p>"


def _item_html(ctx: Context, number: int, item: Item, entry: Mapping[str, Any]) -> str:
    out = [f'<section class="item" id="{_e(item.item_id)}"><h3>{number}. {_e(item.title)}</h3>',
           f'<p class="meta"><code>{_e(entry["item"])}</code> · стр. {_e(item.page)} · {_e(item.region)}</p>',
           f'<p class="flags">{_e("; ".join(item.flags))}</p>', _verdict(entry)]
    out += [_crop_html(ctx, c) for c in crops(item.region, pages_of(item.page))]
    out += [f"<p><b>A:</b> {_e(item.a)}</p>", f"<p><b>B:</b> {_e(item.b)}</p>"]
    if item.notes:
        out.append("<ul class=\"notes\">" + "".join(f"<li>{_e(n)}</li>" for n in item.notes) + "</ul>")
    if item.item_id in ctx.points:
        out.append(_point_html(ctx, ctx.points[item.item_id]))
    out += [_record_html(ctx, key) for key in ctx.records.get(item.item_id, [])]
    if item.kind == "record" and item.item_id not in ctx.records:
        out.append('<p class="none">Записи в черновике нет: вердикт остаётся в листе.</p>')
    out.append("</section>")
    return "".join(out)


def _rows_html(ctx: Context, rows: Sequence[tuple[Item, Mapping[str, Any]]]) -> str:
    first = rows[0][0]
    out = ['<section class="item"><h3>Строки таблицы 5.5</h3>']
    out += [_crop_html(ctx, c) for c in crops(first.region, pages_of(first.page))]
    out.append("<table class=\"rows\"><tr><th>φ_II</th><th>A</th><th>B</th><th>Черновик</th>"
               "<th>Статус</th><th>Вердикт</th></tr>")
    for item, entry in rows:
        values = ", ".join(f"{_record(ctx, k)['value']:g}" for k in ctx.records.get(item.item_id, []))
        out.append(f"<tr><td>{_e(item.item_id.split('=')[1])}</td><td>{_e(item.a)}</td><td>{_e(item.b)}</td>"
                   f"<td>[{values}]</td><td>{_e(item.flags[0])}</td><td>{_verdict(entry)}</td></tr>")
    out.append("</table></section>")
    return "".join(out)


STYLE = """
:root{--bg:#fbfbf9;--fg:#1d1d1b;--muted:#6b6b66;--line:#deded8;--card:#fff;--accent:#c2410c;--calc:#0f5e9c}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--fg:#ececea;--muted:#a3a39d;--line:#34342f;
--card:#1f1f1d;--accent:#fb923c;--calc:#7cc0f5}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px 64px}h1{font-size:22px;margin:0 0 4px}
header p{color:var(--muted);margin:2px 0}.item{background:var(--card);border:1px solid var(--line);
border-radius:8px;padding:16px;margin:20px 0}.item h3{margin:0 0 4px;font-size:17px}
.meta,.flags{color:var(--muted);margin:0;font-size:13px}.crop{margin:12px 0}
.frame{position:relative;border:1px solid var(--line);background:#fff}.frame img{display:block;width:100%}
.whole .frame{max-width:640px}.box{position:absolute;outline:2px solid var(--accent);
background:color-mix(in srgb,var(--accent) 10%,transparent)}figcaption{color:var(--muted);font-size:12px}
.record{border-top:1px dashed var(--line);margin-top:12px;padding-top:8px}.record h4{margin:0 0 6px;font-size:14px}
table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;padding:4px 8px;
border-bottom:1px solid var(--line)}th{color:var(--muted);font-weight:500;width:110px}
.rows th{width:auto}.raw{display:block;color:var(--muted);font-size:12px;margin-top:2px;overflow-wrap:anywhere}
.tex{font-size:17px}code{font-size:13px;overflow-wrap:anywhere}.calc{color:var(--calc)}
.verdict{margin:6px 0}.verdict.empty{color:var(--muted)}.none{color:var(--muted)}.notes{margin:4px 0;
color:var(--muted);font-size:13px}.rows .verdict{margin:0}
"""

SCRIPT = """
document.addEventListener("DOMContentLoaded",()=>{if(!window.katex)return;
document.querySelectorAll(".tex").forEach(el=>{try{katex.render(el.dataset.tex,el,{throwOnError:false})}catch(e){}});});
"""


def render_page(ctx: Context, sheet: Mapping[str, Any], items: Mapping[str, Item], today: date,
                sources: Mapping[str, str]) -> str:
    """Формирует страницу HTML одного листа.

    Страница только для чтения: вердикты пишутся в YAML листа, а здесь показываются
    как есть.

    Args:
        ctx: общие данные.
        sheet: лист порции.
        items: проверки по локальному id.
        today: дата формирования.
        sources: пути PDF, черновика и листа для шапки.

    Returns:
        Текст HTML.
    """
    portion = str(sheet["portion"])
    entries = [(items[str(e["item"]).split("/", 1)[1]], e) for e in sheet["items"]]
    singles = [(i, e) for i, e in entries if i.kind != "table-row"]
    rows = [(i, e) for i, e in entries if i.kind == "table-row"]
    body = [_item_html(ctx, n, i, e) for n, (i, e) in enumerate(singles, start=1)]
    if rows:
        body.append(_rows_html(ctx, rows))
    head = "".join(f"<p>{_e(k)}: <code>{_e(v)}</code></p>" for k, v in sources.items())
    return (
        '<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>Порция {_e(portion)}</title>"
        f'<link rel="stylesheet" href="{KATEX}/katex.min.css">'
        f'<script defer src="{KATEX}/katex.min.js"></script><style>{STYLE}</style><script>{SCRIPT}</script>'
        f"</head><body><main><header><h1>Порция {_e(portion)}</h1>"
        f"<p>Сформировано {today.isoformat()} (<code>python -m extractcmp html</code>). Только просмотр: "
        f"вердикты пишутся в <code>{_e(portion)}.yaml</code>. Рамка — область по выписке B; "
        "совпадение A, B и черновика проверку не снимает.</p>"
        f"{head}</header>{''.join(body)}</main></body></html>\n"
    )
