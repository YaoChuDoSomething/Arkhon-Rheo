"""Calculator Tool Module.

This module provides the CalculatorTool class, which allows agents to
evaluate simple mathematical expressions securely using an AST-based parser
instead of the unsafe built-in ``eval``.
"""

from __future__ import annotations

import ast
import math
import operator
from typing import Any

from arkhon_rheo.tools.base import BaseTool

# ---------------------------------------------------------------------------
# Safe AST evaluator
# ---------------------------------------------------------------------------

_SAFE_OPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_SAFE_FUNCS: dict[str, Any] = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_") and callable(getattr(math, name))
} | {"abs": abs, "round": round}

_MAX_EXPR_LEN = 256


def _safe_eval(node: ast.expr) -> float:
    """Recursively evaluate a safe AST node."""
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported literal type: {type(node.value).__name__}")
        return float(node.value)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _SAFE_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _SAFE_OPS[op_type](_safe_eval(node.operand))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed.")
        func_name = node.func.id
        func = _SAFE_FUNCS.get(func_name)
        if func is None:
            raise ValueError(f"Unknown function: '{func_name}'")
        args = [_safe_eval(a) for a in node.args]
        if node.keywords:
            raise ValueError("Keyword arguments are not supported.")
        return func(*args)
    raise ValueError(f"Unsupported AST node: {type(node).__name__}")


class CalculatorTool(BaseTool):
    """Tool for evaluating mathematical expressions.

    Uses an AST-based evaluator that only permits numeric literals,
    arithmetic operators, and a whitelist of ``math`` functions.  The unsafe
    built-in ``eval`` is not used.
    """

    name = "calculator"
    description = "Evaluate mathematical expressions safely."

    def run(self, **kwargs: Any) -> str:
        """Evaluate a mathematical expression string.

        Args:
            **kwargs: Keyword arguments, expects 'tool_input'.

        Returns:
            The result of the evaluation as a string, or an error message.
        """
        tool_input: str = kwargs.get("tool_input", "")

        if len(tool_input) > _MAX_EXPR_LEN:
            return f"Error: Expression too long (max {_MAX_EXPR_LEN} characters)."

        try:
            tree = ast.parse(tool_input, mode="eval")
            result = _safe_eval(tree.body)
            return str(result)
        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as e:
            return f"Error evaluating expression: {e}"
