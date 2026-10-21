"""Командная строка: сравнение, порции, подпись и перенос вердиктов."""

import argparse
from collections.abc import Sequence
from datetime import date
from pathlib import Path

import yaml

from extractcmp import checkpoints, marks, portions, promote, report
from extractcmp.compare import compare_all
from extractcmp.normalize import load_a, load_b

HERE = Path(__file__).resolve().parent.parent


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
    a_ed = a_data.get("source", {}).get("edition_as_printed", "—")
    b_ed = b_data.get("meta", {}).get("edition", {}).get("printed_header", "—")
    items = [
        *portions.record_items(results),
        portions.edition_item(str(a_ed), str(b_ed)),
        *portions.control_point_items(points, ex1["label"]),
    ]
    parts = portions.split(items)
    pdir = out / "portions"
    pdir.mkdir(exist_ok=True)
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
    p.add_argument("--date", help="ГГГГ-ММ-ДД; по умолчанию сегодня")
    p.set_defaults(func=build)
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
    args = parser.parse_args(argv)
    return args.func(args)
