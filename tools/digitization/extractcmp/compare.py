"""Сравнение записей извлечений A и B."""

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from extractcmp.normalize import Entry, latex_tokens

DIFF_KINDS = ("value", "table-structure", "formula-symbols", "status")
METADATA = "metadata"


@dataclass(frozen=True)
class Finding:
    """Одно найденное различие или односторонее поле.

    Attributes:
        kind: ``value``, ``table-structure``, ``formula-symbols``, ``status`` или ``metadata``
            для различий; ``field-only-a`` и ``field-only-b`` для поля, прочитанного одной
            стороной.
        field: имя поля.
        a: значение в A.
        b: значение в B.
        note: пояснение.
    """

    kind: str
    field: str
    a: Any = None
    b: Any = None
    note: str = ""


@dataclass
class Comparison:
    """Результат сравнения одной пары записей.

    Attributes:
        key: общий идентификатор пары.
        a: запись A или ``None``.
        b: запись B или ``None``.
        findings: различия и односторонние поля.
        matched: сколько сравниваемых полей и ячеек совпало.
        outcome: ``match``, ``partial``, ``image-only``, ``diff``, ``metadata-diff``,
            ``not-found``, ``only-a`` или ``only-b``.
    """

    key: str
    a: Entry | None
    b: Entry | None
    findings: list[Finding] = field(default_factory=list)
    matched: int = 0
    outcome: str = "match"

    @property
    def flags(self) -> list[str]:
        """Статусы ``ambiguous``, ``needs-image`` и ``not-found`` обеих сторон."""
        flags: list[str] = []
        for entry in (self.a, self.b):
            if entry is None:
                continue
            if entry.ambiguous:
                flags.append(f"ambiguous ({entry.source})")
            if entry.status in ("needs-image", "not-found"):
                flags.append(f"{entry.status} ({entry.source})")
        return flags

    @property
    def entry(self) -> Entry:
        """Запись любой из сторон: B, если она есть, иначе A."""
        entry = self.b or self.a
        assert entry is not None
        return entry

    @property
    def priority(self) -> int:
        """0 для расхождений и записей одной стороны, 1 для ambiguous и needs-image, 2 для остальных."""
        if self.outcome in ("diff", "metadata-diff", "only-a", "only-b"):
            return 0
        if self.flags:
            return 1
        return 2


class _Acc:
    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self.matched = 0

    def field(self, name: str, a: Any, b: Any, kind: str = "value") -> None:
        if a is None and b is None:
            return
        if a is None:
            self.findings.append(Finding("field-only-b", name, None, b))
        elif b is None:
            self.findings.append(Finding("field-only-a", name, a, None))
        elif a == b:
            self.matched += 1
        else:
            self.findings.append(Finding(kind, name, a, b))

    def latex(self, a: str | None, b: str | None) -> None:
        if a is None or b is None:
            self.field("latex", a, b)
            return
        ta, tb = latex_tokens(a), latex_tokens(b)
        if ta == tb:
            self.matched += 1
            return
        only_a = list((Counter(ta) - Counter(tb)).elements())
        only_b = list((Counter(tb) - Counter(ta)).elements())
        self.findings.append(
            Finding("formula-symbols", "latex", a, b, f"только в A: {only_a}; только в B: {only_b}")
        )


def _compare_scalar(a: Entry, b: Entry, acc: _Acc) -> None:
    for name in ("parameter", "result_symbol"):
        acc.field(name, a.fields[name], b.fields[name], METADATA)
    acc.field("value", a.fields["value"], b.fields["value"])
    acc.field("unit", a.fields["unit"], b.fields["unit"])
    acc.latex(a.fields["latex"], b.fields["latex"])
    acc.field("condition", a.fields["condition"], b.fields["condition"], "formula-symbols")


def _compare_t54(a: Entry, b: Entry, acc: _Acc) -> None:
    acc.field("parameter", a.fields["parameter"], b.fields["parameter"], METADATA)
    ca, cb = a.fields["columns"], b.fields["columns"]
    if len(ca) != len(cb):
        acc.findings.append(Finding("table-structure", "columns", len(ca), len(cb), "число столбцов"))
    for index, (x, y) in enumerate(zip(ca, cb, strict=False), start=1):
        acc.field(f"col{index}.value", x["value"], y["value"])
        acc.field(f"col{index}.symbol", x["symbol"], y["symbol"], "formula-symbols")
        if x["header"] is not None or y["header"] is not None:
            if x["header"] != y["header"]:
                acc.findings.append(
                    Finding("table-structure", f"col{index}.header", x["header"], y["header"])
                )
            else:
                acc.matched += 1
    na, nb = a.fields["condition_numbers"], b.fields["condition_numbers"]
    if na is not None and nb is not None:
        acc.field("condition.numbers", set(na), set(nb), "table-structure")
    elif nb is not None and a.fields["condition_lost"]:
        acc.findings.append(Finding("field-only-b", "condition", None, nb))


def _compare_t55(a: Entry, b: Entry, acc: _Acc) -> None:
    acc.field("parameter", a.fields["parameter"], b.fields["parameter"], METADATA)
    ra, rb = a.fields["rows"], b.fields["rows"]
    if len(ra) != len(rb):
        acc.findings.append(Finding("table-structure", "rows", len(ra), len(rb), "число строк"))
    if a.fields["selectors"] != b.fields["selectors"]:
        acc.findings.append(
            Finding(
                "table-structure",
                "selectors",
                a.fields["selectors"],
                b.fields["selectors"],
                "набор или порядок значений φ",
            )
        )
    for selector in sorted(set(ra) & set(rb)):
        if len(ra[selector]) != len(rb[selector]):
            acc.findings.append(
                Finding("table-structure", f"row[{selector}].columns", len(ra[selector]), len(rb[selector]))
            )
            continue
        for column, (x, y) in enumerate(zip(ra[selector], rb[selector], strict=True), start=1):
            acc.field(f"row[{selector}].col{column}", x, y)
    sa, sb = a.fields["symbols"], b.fields["symbols"]
    if all(s is None for s in sa) and any(s is not None for s in sb):
        acc.findings.append(Finding("field-only-b", "column symbols", None, sb))
    elif sa != sb:
        acc.findings.append(Finding("formula-symbols", "column symbols", sa, sb))
    else:
        acc.matched += 1


def _compare_notes(a: Entry, b: Entry, acc: _Acc) -> None:
    if b.fields["content"] and not a.fields["content"]:
        acc.findings.append(Finding("field-only-b", "content", None, True))
    elif a.fields["content"] and not b.fields["content"]:
        acc.findings.append(Finding("field-only-a", "content", True, None))
    else:
        acc.matched += 1


_COMPARERS = {
    "scalar": _compare_scalar,
    "bound": _compare_scalar,
    "t54row": _compare_t54,
    "t55": _compare_t55,
    "t54notes": _compare_notes,
}


def _pages_ok(a: Entry, b: Entry) -> bool:
    pa, pb = set(a.pages), set(b.pages)
    return not pa or not pb or pa <= pb or pb <= pa


def compare_pair(key: str, a: Entry, b: Entry) -> Comparison:
    """Сравнивает пару записей.

    Args:
        key: общий идентификатор пары.
        a: запись A.
        b: запись B.

    Returns:
        Результат с различиями и итогом.
    """
    result = Comparison(key, a, b)
    acc = _Acc()
    not_found = (a.status == "not-found", b.status == "not-found")
    if all(not_found):
        result.outcome = "not-found"
        return result
    if any(not_found):
        acc.findings.append(Finding("status", "status", a.status, b.status))
    else:
        _COMPARERS[a.shape](a, b, acc)
    if not _pages_ok(a, b):
        acc.findings.append(Finding(METADATA, "page", a.pages, b.pages))
    if a.clause and b.clause and set(a.clause) != set(b.clause):
        acc.findings.append(Finding(METADATA, "clause", a.clause, b.clause))
    result.findings = acc.findings
    result.matched = acc.matched
    result.outcome = _outcome(acc)
    return result


def _outcome(acc: _Acc) -> str:
    kinds = {f.kind for f in acc.findings}
    if kinds & set(DIFF_KINDS):
        return "diff"
    if METADATA in kinds:
        return "metadata-diff"
    one_sided = kinds & {"field-only-a", "field-only-b"}
    if one_sided:
        return "image-only" if acc.matched == 0 else "partial"
    return "match"


def align(a: Mapping[str, Entry], b: Mapping[str, Entry]) -> tuple[list[tuple[str, Entry | None, Entry | None]], dict[str, str]]:
    """Сопоставляет записи A и B.

    Одинаковые идентификаторы сопоставляются сразу. Строки таблицы 5.4 в B названы иначе,
    чем в A, поэтому они сопоставляются по порядку в файле.

    Args:
        a: записи A.
        b: записи B.

    Returns:
        Пары (общий идентификатор, запись A, запись B) и словарь «идентификатор A →
        идентификатор B» для сопоставленных по порядку.
    """
    aliases: dict[str, str] = {}
    rows_a = [e for e in a.values() if e.shape == "t54row" and e.id not in b]
    rows_b = [e for e in b.values() if e.shape == "t54row" and e.id not in a]
    for x, y in zip(rows_a, rows_b, strict=False):
        aliases[x.id] = y.id
    pairs: list[tuple[str, Entry | None, Entry | None]] = []
    used_b: set[str] = set()
    for entry in a.values():
        other = aliases.get(entry.id, entry.id)
        match = b.get(other)
        if match is not None:
            used_b.add(other)
        pairs.append((other, entry, match))
    for entry in b.values():
        if entry.id not in used_b:
            pairs.append((entry.id, None, entry))
    return pairs, aliases


def compare_all(a: Mapping[str, Entry], b: Mapping[str, Entry]) -> tuple[list[Comparison], dict[str, str]]:
    """Сравнивает два извлечения целиком.

    Args:
        a: записи A.
        b: записи B.

    Returns:
        Сравнения в порядке «расхождения, ambiguous и needs-image, остальные», затем по
        странице и идентификатору, и словарь сопоставления по порядку.
    """
    pairs, aliases = align(a, b)
    results = []
    for key, x, y in pairs:
        if x is None:
            results.append(Comparison(key, None, y, outcome="only-b"))
        elif y is None:
            results.append(Comparison(key, x, None, outcome="only-a"))
        else:
            results.append(compare_pair(key, x, y))
    results.sort(key=lambda r: (r.priority, min(r.entry.pages, default=0), r.key))
    return results, aliases
