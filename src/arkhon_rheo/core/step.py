"""Reasoning Step Module.

This module defines the ReActStep class and StepType enum, which are used
to represent individual units of reasoning (thoughts, actions, and
observations) within the ReAct process.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class StepType(str, Enum):
    """Enumeration of possible reasoning step types."""

    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"


@dataclass
class ReActStep:
    """Represents a single step in the ReAct reasoning process.

    Each step captures a discrete element of the agent's thought process or
    interaction with the environment.

    Attributes:
        step_type: The category of the reasoning step.
        content: The textual content or payload of the step.
        timestamp: The time when the step was created.
        metadata: Optional dictionary for additional contextual data.
    """

    step_type: StepType
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert the reasoning step to a dictionary representation.

        Returns:
            A dictionary containing the step's attributes.
        """
        return {
            "step_type": self.step_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata or {},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReActStep:
        """Create a ReActStep instance from a dictionary.

        Args:
            data: A dictionary containing the step's data.

        Returns:
            A new ReActStep instance.
        """
        return cls(
            step_type=StepType(data["step_type"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata"),
        )
