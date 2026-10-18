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


class FormulaError(ValueError):
    """LaTeX формулы не переводится в формулу Word."""


def _unbox(element: BaseOxmlElement) -> None:
    """Снимает рамку ``m:box``, в которую mathml2omml заключает всю формулу.

    Без неё Word может переносить формулу по знакам операций.

    Args:
        element: элемент ``m:oMath`` с одной рамкой ``m:box`` внутри.
    """
    (box,) = element
    element.remove(box)
    element.extend(box[-1])


def _discard(*args: object, **kwargs: object) -> None:
    """Ничего не печатает: подменяет ``print`` внутри mathml2omml.

    Args:
        args: позиционные аргументы ``print``.
        kwargs: именованные аргументы ``print``.
    """


# mathml2omml prints text it cannot place to stdout. Its module global shadows the builtin, so
# catalog text stays out of the server log without touching sys.stdout of other request threads.
mathml2omml.print = _discard


def _office_math(latex: str) -> str:
    return str(mathml2omml.convert(latex2mathml.converter.convert(latex)))


def omml(formula: Math) -> BaseOxmlElement:
    """Переводит формулу из LaTeX в формулу Word (OMML) через MathML.

    Args:
        formula: формула в LaTeX.

    Returns:
        Элемент ``m:oMath``, который вставляется в абзац как строчная формула.

    Raises:
        FormulaError: если LaTeX не переводится: синтаксис, который не понимает
            latex2mathml или mathml2omml, разметка XML внутри ``\\text{}``, слишком
            глубокая вложенность. LaTeX формул каталога извлечён машиной, поэтому
            такой сбой ожидаем и не должен ронять отчёт.
    """
    try:
        element: BaseOxmlElement = parse_xml(
            _office_math(formula.latex).replace("<m:oMath>", f"<m:oMath {nsdecls('m')}>", 1)
        )
    except Exception as error:
        raise FormulaError(f"the LaTeX of a formula cannot be converted: {type(error).__name__}") from error
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
