from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from app.core.exceptions import ExpressionError


class _Node(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class NumberNode(_Node):
    """Константа, напечатанная в самой формуле, а не коэффициент из таблицы."""

    kind: Literal["number"] = "number"
    value: float


class SymbolNode(_Node):
    """Величина, связанная с входом, параметром или результатом предыдущего шага."""

    kind: Literal["symbol"] = "symbol"
    name: str = Field(min_length=1)


class BinaryNode(_Node):
    kind: Literal["add", "sub", "mul", "div", "pow"]
    left: "ExpressionNode"
    right: "ExpressionNode"


class NegNode(_Node):
    kind: Literal["neg"] = "neg"
    operand: "ExpressionNode"


class CallNode(_Node):
    """Вызов функции; закрытый список разрешённых функций хранит движок."""

    kind: Literal["call"] = "call"
    function: str = Field(min_length=1)
    args: tuple["ExpressionNode", ...] = Field(min_length=1)


ExpressionNode = Annotated[
    NumberNode | SymbolNode | BinaryNode | NegNode | CallNode, Field(discriminator="kind")
]

for _model in (BinaryNode, NegNode, CallNode):
    _model.model_rebuild()

_ADAPTER: TypeAdapter[ExpressionNode] = TypeAdapter(ExpressionNode)


def children(node: ExpressionNode) -> tuple[ExpressionNode, ...]:
    """Возвращает непосредственные операнды узла слева направо.

    Args:
        node: узел дерева выражения.

    Returns:
        Операнды узла; у числа и символа — пустой кортеж.
    """
    if isinstance(node, BinaryNode):
        return (node.left, node.right)
    if isinstance(node, NegNode):
        return (node.operand,)
    if isinstance(node, CallNode):
        return node.args
    return ()


def symbols(tree: ExpressionNode) -> tuple[str, ...]:
    """Перечисляет имена символов дерева, каждое один раз, в порядке первого чтения.

    Args:
        tree: дерево выражения.

    Returns:
        Имена символов.
    """
    found: dict[str, None] = {}
    stack = [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, SymbolNode):
            found.setdefault(node.name)
        stack.extend(reversed(children(node)))
    return tuple(found)


def parse_expression(data: object) -> ExpressionNode:
    """Строит дерево выражения из его JSON-формы (design.md, решение 11).

    Здесь ничего не вычисляется.

    Args:
        data: JSON-форма дерева.

    Returns:
        Дерево выражения.

    Raises:
        ExpressionError: если вид узла вне разрешённого набора, узел некорректен или
            дерево слишком глубоко для проверки.
    """
    try:
        return _ADAPTER.validate_python(data)
    except ValidationError as exc:
        raise ExpressionError(f"invalid expression tree: {exc}") from exc
