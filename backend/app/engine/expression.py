import math
from collections.abc import Callable, Mapping
from types import MappingProxyType

from app.core.exceptions import ExpressionError
from app.schemas.expression import (
    BinaryNode,
    CallNode,
    ExpressionNode,
    NegNode,
    SymbolNode,
    children,
)

MAX_DEPTH = 64
MAX_NODES = 4096


def _min(*args: float) -> float:
    return min(args)


def _max(*args: float) -> float:
    return max(args)


FUNCTIONS: Mapping[str, tuple[int, int | None, Callable[..., float]]] = MappingProxyType(
    {
        "sqrt": (1, 1, math.sqrt),
        "exp": (1, 1, math.exp),
        "ln": (1, 1, math.log),
        "log10": (1, 1, math.log10),
        "sin": (1, 1, math.sin),
        "cos": (1, 1, math.cos),
        "tan": (1, 1, math.tan),
        "abs": (1, 1, math.fabs),
        "min": (2, None, _min),
        "max": (2, None, _max),
    }
)

_BINARY: Mapping[str, Callable[[float, float], float]] = MappingProxyType(
    {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
        "div": lambda a, b: a / b,
        "pow": math.pow,
    }
)


def check_expression(tree: ExpressionNode, bindings: Mapping[str, float]) -> None:
    """Check the whole tree before any node is evaluated (design.md decision 11)."""
    count = 0
    stack: list[tuple[ExpressionNode, int]] = [(tree, 1)]
    while stack:
        node, depth = stack.pop()
        count += 1
        if depth > MAX_DEPTH:
            raise ExpressionError(f"expression tree is deeper than {MAX_DEPTH} levels")
        if count > MAX_NODES:
            raise ExpressionError(f"expression tree has more than {MAX_NODES} nodes")
        if isinstance(node, SymbolNode) and node.name not in bindings:
            raise ExpressionError(f"symbol {node.name!r} has no bound value")
        if isinstance(node, CallNode):
            _check_call(node)
        stack.extend((child, depth + 1) for child in children(node))


def _check_call(node: CallNode) -> None:
    if node.function not in FUNCTIONS:
        raise ExpressionError(f"function {node.function!r} is not allowed")
    least, most, _ = FUNCTIONS[node.function]
    if len(node.args) < least or (most is not None and len(node.args) > most):
        raise ExpressionError(f"function {node.function!r} got {len(node.args)} arguments")


def _evaluate(node: ExpressionNode, bindings: Mapping[str, float]) -> float:
    match node:
        case SymbolNode():
            value = bindings[node.name]
        case BinaryNode():
            value = _BINARY[node.kind](_evaluate(node.left, bindings), _evaluate(node.right, bindings))
        case NegNode():
            value = -_evaluate(node.operand, bindings)
        case CallNode():
            value = FUNCTIONS[node.function][2](*(_evaluate(arg, bindings) for arg in node.args))
        case _:
            value = node.value
    if not math.isfinite(value):
        raise ArithmeticError("not a finite number")
    return value


def evaluate_expression(
    tree: ExpressionNode, bindings: Mapping[str, float], step_id: str
) -> float:
    """Evaluate a checked expression tree; values are in base units, so is the result."""
    check_expression(tree, bindings)
    try:
        return _evaluate(tree, bindings)
    except (ArithmeticError, ValueError) as exc:
        raise ExpressionError(f"step {step_id!r} has no finite value: {exc}") from exc
