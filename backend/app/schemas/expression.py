from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from app.core.exceptions import ExpressionError


class _Node(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class NumberNode(_Node):
    """A constant printed in the formula itself, never a coefficient of a table."""

    kind: Literal["number"] = "number"
    value: float


class SymbolNode(_Node):
    """A quantity bound to an input, a parameter, or the result of an earlier step."""

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
    """A call of a function; the engine keeps the closed list of allowed functions."""

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
    """The direct operands of a node, left to right."""
    if isinstance(node, BinaryNode):
        return (node.left, node.right)
    if isinstance(node, NegNode):
        return (node.operand,)
    if isinstance(node, CallNode):
        return node.args
    return ()


def symbols(tree: ExpressionNode) -> tuple[str, ...]:
    """The symbol names of a tree, each once, in the order they are first read."""
    found: dict[str, None] = {}
    stack = [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, SymbolNode):
            found.setdefault(node.name)
        stack.extend(reversed(children(node)))
    return tuple(found)


def parse_expression(data: object) -> ExpressionNode:
    """Build an expression tree from its JSON form (design.md decision 11).

    A node kind outside the allowed set, a malformed node, or a tree too deep to
    validate fails with an ``ExpressionError``; nothing is evaluated here.
    """
    try:
        return _ADAPTER.validate_python(data)
    except ValidationError as exc:
        raise ExpressionError(f"invalid expression tree: {exc}") from exc
