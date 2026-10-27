"""Контрольные точки для верификатора по примеру ex1 методички."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from extractcmp.normalize import Entry


@dataclass(frozen=True)
class ControlPoint:
    """Контрольная точка: вход и ожидаемый выход.

    Attributes:
        cp_id: идентификатор точки.
        group: группа порций верификатора (``P1``, ``P2``, ``P3`` или отложенная ``D``).
        target: идентификаторы проверяемых записей.
        title: что проверяет точка.
        inputs: входы; ``None`` оставляет поле верификатору.
        expected: ожидаемые выходы; ``None`` оставляет поле верификатору.
        sourced: значения взяты из методички, пометка берётся из данных.
        note: пояснение для верификатора.
    """

    cp_id: str
    group: str
    target: tuple[str, ...]
    title: str
    inputs: Mapping[str, str | None]
    expected: Mapping[str, str | None]
    sourced: bool = False
    note: str = ""


def _row(entry: Entry | None, selector: int) -> list[float] | None:
    if entry is None:
        return None
    values = entry.fields["rows"].get(selector)
    return None if values is None else list(values)


def build(ex1: Mapping[str, Any], a_t55: Entry | None, b_t55: Entry | None) -> list[ControlPoint]:
    """Строит контрольные точки.

    Ожидаемые выходы берутся только из ``ex1``; где методичка их не даёт, поле остаётся
    пустым. Ничего не вычисляется.

    Args:
        ex1: данные примера ``ex1`` из ``data/ex1.yaml``.
        a_t55: запись таблицы 5.5 из A.
        b_t55: запись таблицы 5.5 из B.

    Returns:
        Точки в порядке порций.
    """
    inputs = {name: item["value"] for name, item in ex1["inputs_r"].items()}
    t54, t55 = ex1["table_54"], ex1["table_55"]
    phi = int(t55["phi_ii"])
    guide = [float(t55[n]) for n in ("M_gamma", "M_q", "M_c")]
    row_a, row_b = _row(a_t55, phi), _row(b_t55, phi)
    lookup = (
        f"В извлечениях при φ={phi}: A {row_a}, B {row_b}; методичка {guide}; "
        f"A совпадает с методичкой: {row_a == guide}; B совпадает: {row_b == guide} "
        "(сравнение кодом, не нормативное значение)."
    )
    r1, r2 = ex1["r_initial"], ex1["r_refined"]
    return [
        ControlPoint("CP-R-1", "P1", ("r_formula_5_7",), "R по формуле (5.7), условная ширина",
                     {**inputs, "b": r1["b"]}, {"R": f"{r1['r']} {r1['unit']}"}, True,
                     "Rусл в методичке, шаг 1 раздела 3.2."),
        ControlPoint("CP-R-2", "P1", ("r_formula_5_7",), "R по формуле (5.7), уточнённая ширина (ex1)",
                     {**inputs, "b": r2["b"]}, {"R": f"{r2['r']} {r2['unit']}", "допуск": None}, True,
                     "Допуск назначает верификатор (design.md, открытый вопрос 1)."),
        ControlPoint("CP-R-3", "P1", ("r_formula_5_7",), "R с подвалом (d_b > 0)",
                     {"d_b": None, "остальные входы": None}, {"R": None}, False,
                     "В ex1 d_b = 0; точку и ответ задаёт верификатор."),
        ControlPoint("CP-D1-1", "D", ("d1_formula_5_8",), "d_1 по формуле (5.8)",
                     {"h_s": None, "h_cf": None, "gamma_cf": None, "gamma_II_prime": None}, {"d_1": None}, False,
                     "В ex1 d_1 дано как вход, формула (5.8) в примере не применяется."),
        ControlPoint("CP-KZ-1", "P1", ("k_z_formula_b_below_threshold",), "k_z при b < 10 м (ex1)",
                     {"b": r2["b"]}, {"k_z": inputs["k_z"]}, True),
        ControlPoint("CP-KZ-2", "P1", ("k_z_formula_b_from_threshold",), "k_z при b > 10 м",
                     {"b": None}, {"k_z": None}, False, "В ex1 нет такого b."),
        ControlPoint("CP-K-1", "P1", ("k_direct_tests",), "k при прочностных характеристиках из испытаний (ex1)",
                     {"характеристики": "определены непосредственными испытаниями"}, {"k": inputs["k"]}, True),
        ControlPoint("CP-K-2", "D", ("k_from_appendix_A",), "k при характеристиках по таблицам приложения А",
                     {"характеристики": "приняты по таблицам приложения А"}, {"k": None}, False,
                     "В ex1 такого случая нет."),
        ControlPoint("CP-RULE-1", "D", ("note5_d1_gt_d",), "Примечание 5: d_1 > d",
                     {"d": None, "d_1": None}, {"d_1": None, "d_b": None}, False),
        ControlPoint("CP-RULE-2", "D", ("d_b_cap_2m",), "Подвал глубже 2 м",
                     {"глубина подвала": None}, {"d_b": None}, False),
        ControlPoint("CP-T54-1", "P2", ("t54_clayey_il_gt_0_5",), "Таблица 5.4: суглинок (ex1)",
                     {"I_L": t54["i_l"], "L/H": None}, {"gamma_c1": t54["gamma_c1"], "gamma_c2": t54["gamma_c2"]}, True,
                     "В ex1 L/H не задан; строку таблицы по I_L верификатор указывает сам."),
        ControlPoint("CP-T54-2", "P2", ("t54_notes",), "Таблица 5.4, примечание 3: интерполяция по L/H",
                     {"строка": None, "L/H": None}, {"gamma_c2": None}, False,
                     "Примера с промежуточным L/H в ex1 нет; не вычислять."),
        ControlPoint("CP-T54-3", "P2", ("t54_clayey_il_le_0_25", "t54_clayey_il_0_25_to_0_5"),
                     "Таблица 5.4: граница I_L = 0,25", {"I_L": "0.25"}, {"строка": None}, False,
                     "Граница взята из условий строк в B; к какой строке она относится, решает верификатор."),
        ControlPoint("CP-T54-4", "P2", ("t54_clayey_il_0_25_to_0_5", "t54_clayey_il_gt_0_5"),
                     "Таблица 5.4: граница I_L = 0,5", {"I_L": "0.5"}, {"строка": None}, False,
                     "Граница взята из условий строк в B; к какой строке она относится, решает верификатор."),
        ControlPoint("CP-T55-1", "P2", ("t55",), "Таблица 5.5: φ_II из ex1",
                     {"phi_II": t55["phi_ii"]}, {n: t55[n] for n in ("M_gamma", "M_q", "M_c")}, True, lookup),
        ControlPoint("CP-T55-2", "P2", ("t55",), "Таблица 5.5: первая строка", {"phi_II": "0"},
                     {"M_gamma": None, "M_q": None, "M_c": None}, False, "Крайнее значение диапазона в извлечениях."),
        ControlPoint("CP-T55-3", "P2", ("t55",), "Таблица 5.5: последняя строка", {"phi_II": "45"},
                     {"M_gamma": None, "M_q": None, "M_c": None}, False, "Крайнее значение диапазона в извлечениях."),
        ControlPoint("CP-T55-4", "P2", ("t55",), "Таблица 5.5: промежуточное φ_II",
                     {"phi_II": None}, {"M_gamma": None, "M_q": None, "M_c": None}, False,
                     "Допускает ли норма интерполяцию, решает верификатор; не вычислять."),
        ControlPoint("CP-KZ-3", "P3", ("k_z_threshold_b",), "Граница k_z: b = 10 м",
                     {"b": "10"}, {"k_z": None}, False,
                     "B читает границу как принадлежащую второй ветви (≥); A знак не прочитал."),
        ControlPoint("CP-CHK-1", "P3", ("check_p_le_R",), "Проверка p ≤ R (ex1)",
                     {"p": f"{ex1['check']['p_mean']} {ex1['check']['unit']}",
                      "R": f"{ex1['check']['r']} {ex1['check']['unit']}"},
                     {"условие": ex1["check"]["outcome"]}, True),
        ControlPoint("CP-CHK-2", "P3", ("check_p_le_R",), "Проверка p ≤ R на границе p = R",
                     {"p": None, "R": None}, {"условие": None}, False),
    ]


def render(points: Sequence[ControlPoint], ex1: Mapping[str, Any]) -> str:
    """Формирует документ с контрольными точками.

    Args:
        points: контрольные точки.
        ex1: данные ``ex1`` (источник и пометка).

    Returns:
        Текст Markdown.
    """
    label = ex1["label"]
    out = [
        "# Контрольные точки для верификатора",
        "",
        f"Значения, помеченные «{label}», перенесены из методички как напечатаны "
        f"({ex1['citation']}; карточка {ex1['card']}; страницы: {ex1['pages']}). "
        "Остальные ожидаемые выходы пусты: их заполняет верификатор по нормативу. "
        "Скрипт ничего не вычисляет.",
        "",
        "| Точка | Порция | Проверяет | Вход | Ожидаемый выход | Источник |",
        "|---|---|---|---|---|---|",
    ]
    for p in points:
        source = label if p.sourced else "пусто, заполняет верификатор"
        out.append(
            f"| {p.cp_id} | {p.group} | {', '.join(p.target)} | {_fmt(p.inputs)} | {_fmt(p.expected)} | {source} |"
        )
    notes = [(p.cp_id, p.note) for p in points if p.note]
    out += ["", "## Пояснения", ""] + [f"- {cp_id}: {note}" for cp_id, note in notes]
    return "\n".join(out) + "\n"


def _fmt(values: Mapping[str, str | None]) -> str:
    return "; ".join(f"{k} = {v if v is not None else '…'}" for k, v in values.items())
