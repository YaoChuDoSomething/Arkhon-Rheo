from arkhon_rheo.core.rules.base import BaseRule
from arkhon_rheo.core.state import ReActState
from typing import Optional


class MaxDepthRule(BaseRule):
    """Limit the number of steps in the conversation."""

    def __init__(self, max_steps: int = 10):
        super().__init__(name="MaxDepth")
        self.max_steps = max_steps

    def check(self, state: ReActState) -> Optional[str]:
        steps = state.metadata.get("step_count", 0)
        # Using simple integer comparison for step count
        # In a real system, we might inspect trace history length
        if isinstance(steps, int) and steps > self.max_steps:
            return f"Step count {steps} exceeds maximum of {self.max_steps}."
        return None


class ForbidGuessingRule(BaseRule):
    """Example rule to forbid specific phrases indicating guessing."""

    forbidden = ["i guess", "maybe", "i think"]

    def __init__(self) -> None:
        super().__init__(name="ForbidGuessing")

    def check(self, state: ReActState) -> Optional[str]:
        if not state.thought:
            return None

        thought_lower = state.thought.lower()
        for phrase in self.forbidden:
            if phrase in thought_lower:
                return f"Thought contains forbidden guess phrase: '{phrase}'."
        return None


class CostLimitRule(BaseRule):
    """Limit the accumulated cost."""

    def __init__(self, max_cost: float = 1.0):
        super().__init__(name="CostLimit")
        self.max_cost = max_cost

    def check(self, state: ReActState) -> Optional[str]:
        cost = state.metadata.get("total_cost", 0.0)
        if isinstance(cost, (int, float)) and cost > self.max_cost:
            return f"Total cost {cost} exceeds limit of {self.max_cost}."
        return None
