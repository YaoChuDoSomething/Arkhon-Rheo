from dataclasses import dataclass, replace, field
from typing import Optional, Dict, Any
from types import MappingProxyType


@dataclass(frozen=True)
class ReActState:
    """
    Immutable container for ReAct agent state.

    Attributes:
        thought (Optional[str]): The current thought or reasoning trace.
        action (Optional[str]): The action to be performed (tool call).
        observation (Optional[str]): The result of the action (tool output).
        metadata (Dict[str, Any]): Additional extensive state or context.
    """

    thought: Optional[str] = None
    action: Optional[str] = None
    observation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(self, "metadata", MappingProxyType(self.metadata))

    def with_thought(self, thought: str) -> "ReActState":
        """Return a new state with updated thought."""
        return replace(self, thought=thought)

    def with_action(self, action: str) -> "ReActState":
        """Return a new state with updated action."""
        return replace(self, action=action)

    def with_observation(self, observation: str) -> "ReActState":
        """Return a new state with updated observation."""
        return replace(self, observation=observation)

    def with_metadata(self, metadata: Dict[str, Any]) -> "ReActState":
        """Return a new state with updated metadata."""
        # Merge new metadata with existing one or replace?
        # Typically "with_" methods replace the value.
        # But for metadata, users might want to merge.
        # Use replace for consistency with other fields.
        return replace(self, metadata=metadata)
