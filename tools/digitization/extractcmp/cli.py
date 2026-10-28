"""Командная строка: сравнение, порции, подпись и перенос вердиктов."""

import argparse
from collections.abc import Sequence
from datetime import date
from pathlib import Path

import yaml

from extractcmp import checkpoints, draft, marks, portions, promote, report, viewer
from extractcmp.compare import compare_all
from extractcmp.normalize import load_a, load_b

HERE = Path(__file__).resolve().parent.parent
SHEETS_DIR = HERE.parent.parent / "docs" / "verification" / "interim-normatives-source"
"""Отслеживаемая git папка листов: ``promote`` требует коммита листа подписавшим."""
DOCUMENT = HERE / "data" / "document.yaml"
"""Сведения о документе, которые дал верификатор: где напечатан перечень изменений."""


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _dump(data: object) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


def build(args: argparse.Namespace) -> int:
    """Строит отчёт сравнения, пометки изменений, контрольные точки и порции.

    Args:
        args: разобранные аргументы подкоманды ``build``.

    Returns:
        Код выхода.
    """
    a_data, b_data = _load(args.a), _load(args.b)
    a, b = load_a(a_data), load_b(b_data)
    results, aliases = compare_all(a, b)
    today = date.fromisoformat(args.date) if args.date else date.today()
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / "diff-report.md").write_text(
        report.render(
            results, aliases, report.edition_map(a), report.edition_map(b), today,
            _rel(args.a), _rel(args.b),
        ),
        encoding="utf-8",
    )
    a_report = args.a.with_name(args.a.stem + ".report.md")
    b_report = args.b.with_name(args.b.stem + ".report.md")
    (out / "amendment-marks.md").write_text(
        marks.render(
            a, b, b_data.get("amendment_marks", []),
            a_report.read_text(encoding="utf-8") if a_report.exists() else "",
            b_report.read_text(encoding="utf-8") if b_report.exists() else "",
        ),
        encoding="utf-8",
    )
    ex1 = _load(args.ex1)
    points = checkpoints.build(ex1, a.get("t55"), b.get("t55"))
    (out / "control-points.md").write_text(checkpoints.render(points, ex1), encoding="utf-8")
    items = _items(a_data, b_data, results, points, ex1)
    parts = portions.split(items)
    pdir = args.sheets_dir
    pdir.mkdir(parents=True, exist_ok=True)
    sources = {"a": _rel(args.a), "b": _rel(args.b)}
    for portion in parts:
        (pdir / f"{portion.portion_id}.md").write_text(
            portions.render_markdown(portion, today, ex1["label"]), encoding="utf-8"
        )
        (pdir / f"{portion.portion_id}.yaml").write_text(
            _dump(portions.render_sheet(portion, today, sources)), encoding="utf-8"
        )
    (pdir / "index.md").write_text(portions.render_index(parts, today), encoding="utf-8")
    counts = report.summary(results)
    print(dict(counts), f"portions={len(parts)}", f"minutes={sum(p.minutes for p in parts):.0f}")
    return 0


def _items(a_data: dict, b_data: dict, results: list, points: list, ex1: dict) -> list[portions.Item]:
    a_ed = a_data.get("source", {}).get("edition_as_printed", "—")
    b_ed = b_data.get("meta", {}).get("edition", {}).get("printed_header", "—")
    place = _load(DOCUMENT).get("edition", {}) if DOCUMENT.exists() else {}
    where = {k: str(place[k]) for k in ("page", "region") if k in place}
    return [
        *portions.record_items(results),
        portions.edition_item(str(a_ed), str(b_ed), **where),
        *portions.control_point_items(points, ex1["label"]),
    ]


def make_draft(args: argparse.Namespace) -> int:
    """Собирает черновик файла типа и сопоставление записей с листами.

    Args:
        args: разобранные аргументы подкоманды ``draft``.

    Returns:
        Код выхода.
    """
    a_data, b_data = _load(args.a), _load(args.b)
    a, b = load_a(a_data), load_b(b_data)
    results, _ = compare_all(a, b)
    ex1 = _load(args.ex1)
    points = checkpoints.build(ex1, a.get("t55"), b.get("t55"))
    items = {i.item_id: i for i in _items(a_data, b_data, results, points, ex1)}
    result = draft.build(b, items)
    today = date.fromisoformat(args.date) if args.date else date.today()
    args.out.write_text(_dump(result.type_file), encoding="utf-8")
    args.mapping_out.write_text(_dump(result.mapping), encoding="utf-8")
    args.notes_out.write_text(draft.render_notes(result, today.isoformat()), encoding="utf-8")
    print({name: len(rows) for name, rows in result.type_file.items()}, f"not_stored={len(result.not_stored)}")
    return 0


def make_html(args: argparse.Namespace) -> int:
    """Строит страницы HTML листов: вырезки PDF, выписки и записи черновика.

    Args:
        args: разобранные аргументы подкоманды ``html``.

    Returns:
        Код выхода.
    """
    a_data, b_data = _load(args.a), _load(args.b)
    a, b = load_a(a_data), load_b(b_data)
    results, _ = compare_all(a, b)
    ex1 = _load(args.ex1)
    points = checkpoints.build(ex1, a.get("t55"), b.get("t55"))
    items = {i.item_id: i for i in _items(a_data, b_data, results, points, ex1)}
    ctx = viewer.context(_load(args.draft), _load(args.mapping), points, viewer.pdftoppm(args.pdf))
    today = date.fromisoformat(args.date) if args.date else date.today()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for path in args.sheets:
        sheet = _load(path)
        sources = {"PDF": _rel(args.pdf), "черновик": _rel(args.draft), "лист": _rel(path)}
        out = args.out_dir / f"{sheet['portion']}.html"
        out.write_text(viewer.render_page(ctx, sheet, items, today, sources), encoding="utf-8")
        print(out)
    return 0


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(HERE.parent.parent))
    except ValueError:
        return str(path)


def sign(args: argparse.Namespace) -> int:
    """Подписывает заполненный лист проверки.

    Args:
        args: разобранные аргументы подкоманды ``sign``.

    Returns:
        Код выхода.
    """
    sheet = _load(args.sheet)
    args.sheet.write_text(
        _dump(promote.sign_sheet(sheet, args.by, date.fromisoformat(args.at))), encoding="utf-8"
    )
    return 0


def apply(args: argparse.Namespace) -> int:
    """Переносит вердикты подписанных листов в черновик данных.

    Args:
        args: разобранные аргументы подкоманды ``promote``.

    Returns:
        Код выхода: 0, если перенос выполнен; 1, если лист не принят.
    """
    manifest = _load(args.manifest)
    verifiers = manifest.get("verifiers", [])
    sheets = [_load(path) for path in args.sheets]
    errors = []
    for path, sheet in zip(args.sheets, sheets, strict=True):
        signature = sheet.get("signature") or {}
        errors += [f"{path}: {e}" for e in promote.check_committed(path, str(signature.get("by")))]
    if errors:
        print("\n".join(errors))
        return 1
    try:
        result, lines = promote.promote(_load(args.draft), _load(args.mapping), sheets, verifiers)
    except ValueError as error:
        print(error)
        return 1
    args.out.write_text(_dump(result), encoding="utf-8")
    print("\n".join(lines))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Точка входа.

    Args:
        argv: аргументы командной строки; по умолчанию ``sys.argv``.

    Returns:
        Код выхода.
    """
    root = HERE.parent.parent / "docs" / "akim" / "digitization"
    parser = argparse.ArgumentParser(prog="extractcmp")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("build", help="отчёт сравнения, пометки, контрольные точки, порции")
    p.add_argument("--a", type=Path, default=root / "extract-a.yaml")
    p.add_argument("--b", type=Path, default=root / "extract-b.yaml")
    p.add_argument("--ex1", type=Path, default=HERE / "data" / "ex1.yaml")
    p.add_argument("--out-dir", type=Path, default=root)
    p.add_argument("--sheets-dir", type=Path, default=SHEETS_DIR, help="листы порций и их оглавление")
    p.add_argument("--date", help="ГГГГ-ММ-ДД; по умолчанию сегодня")
    p.set_defaults(func=build)
    p = sub.add_parser("draft", help="черновик файла типа и сопоставление с листами")
    p.add_argument("--a", type=Path, default=root / "extract-a.yaml")
    p.add_argument("--b", type=Path, default=root / "extract-b.yaml")
    p.add_argument("--ex1", type=Path, default=HERE / "data" / "ex1.yaml")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--mapping-out", type=Path, default=root / "draft-mapping.yaml")
    p.add_argument("--notes-out", type=Path, default=root / "draft-notes.md")
    p.add_argument("--date", help="ГГГГ-ММ-ДД; по умолчанию сегодня")
    p.set_defaults(func=make_draft)
    p = sub.add_parser("sign", help="подписать заполненный лист (выполняет верификатор)")
    p.add_argument("sheet", type=Path)
    p.add_argument("--by", required=True)
    p.add_argument("--at", required=True, help="ГГГГ-ММ-ДД")
    p.set_defaults(func=sign)
    p = sub.add_parser("promote", help="перенести вердикты подписанных листов в черновик")
    p.add_argument("--draft", type=Path, required=True)
    p.add_argument("--mapping", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("sheets", type=Path, nargs="+")
    p.set_defaults(func=apply)
    p = sub.add_parser("html", help="страницы листов с вырезками PDF (только просмотр)")
    p.add_argument("--a", type=Path, default=root / "extract-a.yaml")
    p.add_argument("--b", type=Path, default=root / "extract-b.yaml")
    p.add_argument("--ex1", type=Path, default=HERE / "data" / "ex1.yaml")
    p.add_argument("--draft", type=Path, required=True)
    p.add_argument("--mapping", type=Path, default=root / "draft-mapping.yaml")
    p.add_argument("--pdf", type=Path, default=HERE.parent.parent / "docs" / "NTD" / "СП 22.13330.2016.pdf")
    p.add_argument("--out-dir", type=Path, default=root / "sheets-html",
                   help="вне git: в страницах вырезки текста нормы")
    p.add_argument("--date", help="ГГГГ-ММ-ДД; по умолчанию сегодня")
    p.add_argument("sheets", type=Path, nargs="+")
    p.set_defaults(func=make_html)
    args = parser.parse_args(argv)
    return args.func(args)
