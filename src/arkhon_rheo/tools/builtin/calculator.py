"""Calculator Tool Module.

This module provides the CalculatorTool class, which allows agents to
evaluate simple mathematical expressions securely.
"""

from __future__ import annotations

import math
from typing import Any

from arkhon_rheo.tools.base import BaseTool


class CalculatorTool(BaseTool):
    """Tool for evaluating mathematical expressions.

    Uses a constrained evaluation environment to safely process basic arithmetic
    and mathematical functions.
    """

    name = "calculator"
    description = "Evaluate mathematical expressions safely."

    def run(self, input: str, **kwargs: Any) -> str:
        """Evaluate a mathematical expression string.

        Args:
            input: The mathematical expression to evaluate (e.g., "2 + 2").
            **kwargs: Additional keyword arguments (ignored).

        Returns:
            The result of the evaluation as a string, or an error message.
        """
        try:
            # Check for unsafe imports or double underscores
            if "__" in input or "import" in input:
                return "Error: Unsafe expression detected."

            # Allowed globals for the evaluation environment
            allowed_names = {"math": math, "abs": abs, "round": round}

            # Constrained evaluation
            result = eval(input, {"__builtins__": None}, allowed_names)
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {e}"
