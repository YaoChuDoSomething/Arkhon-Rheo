from pydantic import BaseModel, Field
from arkhon_rheo.tools.base import BaseTool
import math


class CalculatorInput(BaseModel):
    expression: str = Field(
        description="Mathematical expression to evaluate (e.g. '2 + 2')"
    )


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate mathematical expressions."
    args_schema = CalculatorInput

    def run(self, expression: str) -> str:  # type: ignore[override]
        try:
            # Dangerous in production, but okay for stub/MVP if constrained
            # A real implementation should use a safe parser like `numexpr` or limited recursive descent parser
            # For now, we stub it or use eval with very restricted globals
            allowed_names = {"math": math, "abs": abs, "round": round}
            result = eval(expression, {"__builtins__": None}, allowed_names)
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {e}"
