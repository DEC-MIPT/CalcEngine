import pytest
from docx import Document
from docx.oxml.ns import qn

from app.reporting.docx_writer import step_lines, write_line
from app.reporting.format import (
    UNIT_DESIGNATIONS,
    check_rounding,
    compact_norm_refs,
    format_norm_ref,
    format_number,
    format_parameter_source,
    latex_number,
    latex_quantity,
)
from app.schemas.calculation import (
    CATALOG_SOURCE,
    CheckStep,
    NormRef,
    ParameterSourceInfo,
    QuantityValue,
    RoundingRule,
    Substitution,
)
from app.schemas.units import UNITS


@pytest.mark.parametrize(
    ("value", "text"),
    [
        (172.5, "172,5"),
        (1e-07, "0,0000001"),
        (2.0, "2"),
        (100.0, "100"),
        (1e20, "100000000000000000000"),
        (0.1 + 0.2, "0,30000000000000004"),
        (-3.25, "-3,25"),
        (-0.0, "0"),
    ],
)
def test_a_number_is_the_shortest_decimal_without_an_exponent_with_a_comma(value: float, text: str) -> None:
    assert format_number(value) == text


HUNDREDTHS = RoundingRule(decimals=2, mode="half_up")


@pytest.mark.parametrize(
    ("value", "decimals", "text"),
    [(172.5, 2, "172,50"), (168.29, 2, "168,29"), (0.0, 2, "0,00"), (-0.0, 1, "0,0"), (2.0, 0, "2"), (0.125, 1, "0,125")],
)
def test_a_number_is_padded_to_the_given_decimals(value: float, decimals: int, text: str) -> None:
    assert format_number(value, decimals) == text


@pytest.mark.parametrize(("value", "text"), [(172.5, "172{,}5"), (2.0, "2"), (-3.25, "-3{,}25")])
def test_a_latex_number_keeps_its_comma_in_braces(value: float, text: str) -> None:
    assert latex_number(value) == text


@pytest.mark.parametrize(
    ("value", "unit", "text"),
    [
        (172.5, "kPa", r"172{,}5\ \text{кПа}"),
        (1e-07, "m", r"0{,}0000001\ \text{м}"),
        (2.0, "1", "2"),
        (20.0, "deg", r"20\text{°}"),
    ],
)
def test_a_latex_quantity_prints_with_the_russian_designation_of_its_unit(value: float, unit: str, text: str) -> None:
    assert latex_quantity(QuantityValue(value=value, unit=unit)) == text


@pytest.mark.parametrize(
    ("value", "text"), [(168.28900000000002, r"168{,}29\ \text{кПа}"), (172.5, r"172{,}50\ \text{кПа}")]
)
def test_an_output_value_prints_rounded_with_exactly_its_decimals(value: float, text: str) -> None:
    assert latex_quantity(QuantityValue(value=value, unit="kPa"), HUNDREDTHS) == text


UNVERIFIED = NormRef(
    document="<DOC>", edition="unverified", clause="<CLAUSE>", status="unverified", provenance="machine-extracted"
)


def check(result: float, right: float, passed: bool) -> CheckStep:
    return CheckStep(
        step_id="check",
        expression=r"y \le y_{lim}",
        substitutions=(
            Substitution(symbol="y", value=result, unit="kPa"),
            Substitution(symbol="y_lim", value=right, unit="kPa"),
        ),
        result=QuantityValue(value=result, unit="kPa"),
        operator="le",
        right=QuantityValue(value=right, unit="kPa"),
        passed=passed,
        norm_refs=(UNVERIFIED,),
    )


def test_a_check_side_that_is_an_output_follows_its_rule() -> None:
    assert check_rounding(check(100.0, 168.289, True), {"y_lim": HUNDREDTHS}) == (None, HUNDREDTHS)
    assert check_rounding(check(100.0, 168.289, True), {}) == (None, None)


def test_a_check_prints_unrounded_when_rounding_would_contradict_its_outcome() -> None:
    assert check_rounding(check(4.996, 4.999, True), {"y": HUNDREDTHS}) == (None, None)


def test_demo_comparison_preserves_output_precedence_and_keeps_decisive_precision() -> None:
    thousandths = RoundingRule(decimals=3, mode="half_even")
    assert check_rounding(check(3.75, 4.25, True), {"y": thousandths}, HUNDREDTHS) == (thousandths, HUNDREDTHS)
    assert check_rounding(check(4.001, 4, False), {}, HUNDREDTHS) == (None, None)


@pytest.mark.parametrize(("step", "rules", "expected"), [
    (check(2.675, 4, True), {}, "2,68 кПа≤4,00 кПа"),
    (check(3.75, 4.25, True), {"y": RoundingRule(decimals=3, mode="half_even")}, "3,750 кПа≤4,25 кПа"),
    (check(4.001, 4, False), {}, "4,001 кПа≤4 кПа"),
])
def test_demo_docx_comparison_is_office_math_with_correct_precision(
    step: CheckStep, rules: dict[str, RoundingRule], expected: str,
) -> None:
    lines = step_lines(1, step, {}, rules, HUNDREDTHS)
    paragraph = Document().add_paragraph()
    write_line(paragraph, next(line for line in lines if line[0] == "Сравнение: "))
    assert paragraph._p.xpath("./m:oMath")
    math = "".join(node.text or "" for node in paragraph._p.iter(qn("m:t"))).replace("\xa0", " ")
    assert math == expected


def test_compact_sp22_refs_keep_distinct_editions_and_statuses() -> None:
    table = NormRef(document="СП 22.13330.2016", edition="2016", clause="таблица 5.4",
                    status="verified", provenance="human-verified")
    formula = NormRef(document=table.document, edition=table.edition, clause="unverified",
                      status="unverified", provenance="machine-extracted")
    other_edition = formula.model_copy(update={"edition": "unverified"})
    assert compact_norm_refs((table, formula, table, other_edition, UNVERIFIED), status=True) == (
        "СП 22.13330.2016, редакция: 2016: таблица 5.4 (статус: проверено); не проверено (статус: не проверено)",
        format_norm_ref(other_edition), format_norm_ref(UNVERIFIED),
    )


def test_every_unit_of_the_vocabulary_has_a_russian_designation() -> None:
    assert set(UNIT_DESIGNATIONS) == set(UNITS)
    assert [unit for unit, designation in UNIT_DESIGNATIONS.items() if not designation] == ["1"]


def test_a_norm_ref_prints_with_its_status_and_unverified_parts() -> None:
    unverified = NormRef(
        document="<DOC>", edition="unverified", clause="<CLAUSE>", status="unverified", provenance="machine-extracted"
    )
    verified = NormRef(document="<DOC>", edition="<ED>", clause="<CLAUSE>", status="verified", provenance="human-verified")

    assert format_norm_ref(unverified) == "<DOC>, редакция: не проверено, пункт: <CLAUSE> (статус: не проверено)"
    assert format_norm_ref(verified) == "<DOC>, редакция: <ED>, пункт: <CLAUSE> (статус: проверено)"
    assert format_norm_ref(unverified, status=False) == "<DOC>, редакция: не проверено, пункт: <CLAUSE>"


@pytest.mark.parametrize(
    ("source", "text"),
    [
        (CATALOG_SOURCE, "Источник нормативных параметров: каталог норм."),
        (
            ParameterSourceInfo(kind="interim", data_sha256="f" * 64, profile="draft"),
            f"Источник нормативных параметров: временные нормативные данные, профиль draft, SHA-256 данных {'f' * 64}.",
        ),
    ],
    ids=["catalog", "interim-draft"],
)
def test_the_parameter_source_prints_its_kind_and_for_interim_data_the_profile_and_the_full_digest(
    source: ParameterSourceInfo, text: str
) -> None:
    assert format_parameter_source(source) == text
