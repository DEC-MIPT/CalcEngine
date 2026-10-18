from dataclasses import dataclass

import latex2mathml.converter
import mathml2omml
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.oxml.xmlchemy import BaseOxmlElement


@dataclass(frozen=True)
class Math:
    """Формула в LaTeX, которую отчёт печатает формулой Word.

    Attributes:
        latex: выражение LaTeX без ограничителей ``$``.
        breakable: может ли Word переносить формулу на знаках операций; иначе она
            переносится на новую строку целиком.
    """

    latex: str
    breakable: bool = False


Segment = str | Math
"""Часть строки отчёта: обычный текст или формула."""

Line = tuple[Segment, ...]
"""Строка отчёта: абзац или ячейка таблицы из текста и формул по порядку."""


def _unbox(element: BaseOxmlElement) -> None:
    """Снимает рамку ``m:box``, в которую mathml2omml заключает всю формулу.

    Без неё Word может переносить формулу по знакам операций.
    """
    (box,) = element
    element.remove(box)
    element.extend(box[-1])


def omml(formula: Math) -> BaseOxmlElement:
    """Переводит формулу из LaTeX в формулу Word (OMML) через MathML.

    Args:
        formula: формула в LaTeX.

    Returns:
        Элемент ``m:oMath``, который вставляется в абзац как строчная формула.
    """
    mathml = latex2mathml.converter.convert(formula.latex)
    element: BaseOxmlElement = parse_xml(
        mathml2omml.convert(mathml).replace("<m:oMath>", f"<m:oMath {nsdecls('m')}>", 1)
    )
    if formula.breakable:
        _unbox(element)
    return element


def omml_paragraph(formula: Math) -> BaseOxmlElement:
    """Делает из формулы выключенную формулу, прижатую влево, как текст абзаца.

    Word выключает формулу, которая одна в абзаце, и по умолчанию ставит её по центру.

    Args:
        formula: формула в LaTeX.

    Returns:
        Элемент ``m:oMathPara`` с выравниванием влево.
    """
    paragraph: BaseOxmlElement = parse_xml(
        f'<m:oMathPara {nsdecls("m")}><m:oMathParaPr><m:jc m:val="left"/></m:oMathParaPr></m:oMathPara>'
    )
    paragraph.append(omml(formula))
    return paragraph
