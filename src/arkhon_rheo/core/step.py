from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class StepType(str, Enum):
    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    # SYSTEM = "system" # Reserved for future use


@dataclass
class ReActStep:
    """
    Represents a single step in the ReAct reasoning process.
    """

    step_type: StepType
    content: str
    timestamp: datetime = datetime.now()
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary."""
        return {
            "step_type": self.step_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata or {},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReActStep":
        """Create step from dictionary."""
        return cls(
            step_type=StepType(data["step_type"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata"),
        )
