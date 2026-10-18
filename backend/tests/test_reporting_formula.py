from docx.oxml.ns import qn
from test_reporting_docx import visible_text

from app.reporting.formula import Math, omml, omml_paragraph


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
