import pytest
from docx import Document
from docx.oxml.ns import qn
from test_reporting_docx import visible_text

from app.reporting import formula as formula_module
from app.reporting.docx_writer import write_line
from app.reporting.formula import FormulaError, Line, Math, omml, omml_paragraph


def test_a_formula_becomes_an_inline_word_equation() -> None:
    element = omml(Math(r"R = \frac{\gamma_{c1}}{k}"))

    assert element.tag == qn("m:oMath")
    assert next(element.iter(qn("m:f")), None) is not None
    assert visible_text(element) == "R=γc1k"


def test_a_formula_is_kept_whole_unless_it_may_break() -> None:
    whole, breakable = omml(Math("p = 2 b")), omml(Math("p = 2 b", breakable=True))

    assert [child.tag for child in whole] == [qn("m:box")]
    assert qn("m:box") not in [child.tag for child in breakable]
    assert visible_text(whole) == visible_text(breakable) == "p=2b"


def test_a_single_symbol_loses_its_box_too() -> None:
    assert [child.tag for child in omml(Math("k", breakable=True))] == [qn("m:r")]


def test_a_formula_paragraph_is_set_flush_left() -> None:
    paragraph = omml_paragraph(Math("b"))

    justification = paragraph.find(f"{qn('m:oMathParaPr')}/{qn('m:jc')}")
    assert paragraph.tag == qn("m:oMathPara")
    assert justification is not None and justification.get(qn("m:val")) == "left"
    assert [child.tag for child in paragraph][1:] == [qn("m:oMath")]


UNCONVERTIBLE = [
    r"R = \frac{a}{",
    r"R = \text{a & b}",
    r"R = \text{x<y}",
    r"\text{<script>}",
    "{" * 300 + "x" + "}" * 300,
]


@pytest.mark.parametrize("latex", UNCONVERTIBLE)
def test_latex_that_cannot_be_converted_raises_a_formula_error(latex: str) -> None:
    with pytest.raises(FormulaError):
        omml(Math(latex))


def test_the_converter_prints_nothing_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    converted = formula_module.mathml2omml.convert("<math><mrow>stray catalog text<mi>a</mi></mrow></math>")

    assert "<m:t>a</m:t>" in converted
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    ("line", "text"),
    [
        ((Math(r"\frac{a}{"),), r"\frac{a}{"),
        (("Выражение: ", Math(r"R = \text{x<y}", breakable=True), "."), r"Выражение: R = \text{x<y}."),
        ((Math("a\x01b"),), "a\ufffdb"),
        ((Math("a\ufffeb"),), "a\ufffdb"),
    ],
)
def test_a_formula_that_cannot_be_converted_prints_as_its_latex(line: Line, text: str) -> None:
    paragraph = Document().add_paragraph()

    write_line(paragraph, line)

    assert visible_text(paragraph._p) == text
    assert next(paragraph._p.iter(qn("m:oMath")), None) is None
