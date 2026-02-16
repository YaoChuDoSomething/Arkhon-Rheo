import pytest  # ty:ignore[unresolved-import]
from unittest.mock import MagicMock
from dataclasses import dataclass
from datetime import datetime


# Mocking Arkhon-Rheo core structures for verification
@dataclass(frozen=True, slots=True)
class ReasoningStep:
    id: int
    thought: str | None
    action: str | None = None
    observation: str | None = None
    status: str = "draft"
    timestamp: datetime = datetime.now()


class ReActState:
    def __init__(self, steps=None, metadata=None):
        self.steps = steps or []
        self.metadata = metadata or {}


class ForbidGuessingRule:
    """Flag thoughts containing uncertainty markers."""

    name = "forbid_guessing"
    UNCERTAINTY_PHRASES = ["maybe", "probably", "I guess", "might be", "could be"]

    def check(self, step: ReasoningStep, state: ReActState) -> bool:
        if not step.thought:
            return True
        thought = step.thought.lower()
        return not any(phrase in thought for phrase in self.UNCERTAINTY_PHRASES)


def test_forbid_guessing_rule_violation():
    rule = ForbidGuessingRule()
    state = ReActState()

    # Violating thought
    bad_step = ReasoningStep(
        id=1, thought="Maybe the directory is empty because of a git ignore."
    )
    assert rule.check(bad_step, state) is False


def test_forbid_guessing_rule_success():
    rule = ForbidGuessingRule()
    state = ReActState()

    # Compliant thought
    good_step = ReasoningStep(
        id=1, thought="The directory is confirmed empty by the list_dir tool."
    )
    assert rule.check(good_step, state) is True


if __name__ == "__main__":
    # Simple manual run
    rule = ForbidGuessingRule()
    test_thought = "Maybe this works."
    print(f"Testing thought: '{test_thought}'")
    print(
        f"Pass: {rule.check(ReasoningStep(id=0, thought=test_thought), ReActState())}"
    )
