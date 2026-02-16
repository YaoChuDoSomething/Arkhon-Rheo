from arkhon_rheo.core.tools.base import BaseTool
import math


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate mathematical expressions."

    def run(self, input: str) -> str:
        try:
            # Check for unsafe imports or double underscores
            if "__" in input or "import" in input:
                return "Error: Unsafe expression detected."

            # Allowed globals
            allowed_names = {"math": math, "abs": abs, "round": round}
            # dangerous eval, but constrained slightly
            result = eval(input, {"__builtins__": None}, allowed_names)
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {e}"
