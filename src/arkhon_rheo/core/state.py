from dataclasses import dataclass, replace, field
from typing import Optional, Dict, Any, List
from types import MappingProxyType


@dataclass(frozen=True)
class ReasoningStep:
    """
    Immutable event log unit representing a single step in the reasoning process.

    Attributes:
        step_id (str): Unique identifier for this step.
        type (str): Type of step (thought, action, observation, etc.).
        content (str): The main content/payload of the step.
        tool_name (Optional[str]): Name of tool if action.
        tool_input (Optional[Dict[str, Any]]): Input to tool if action.
        tool_output (Optional[Any]): Result of tool if observation.
        timestamp (float): Unix timestamp of when step occurred.
        metadata (Dict[str, Any]): Additional context.
    """

    step_id: str
    type: str
    content: str
    timestamp: float
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(self, "metadata", MappingProxyType(self.metadata))


@dataclass(frozen=True)
class ReActState:
    """
    Immutable container for ReAct agent state.

    Attributes:
        thought (Optional[str]): The current thought or reasoning trace.
        action (Optional[str]): The action to be performed (tool call).
        observation (Optional[str]): The result of the action (tool output).
        metadata (Dict[str, Any]): Additional extensive state or context.
        steps (List[ReasoningStep]): History of all reasoning steps.
    """

    thought: Optional[str] = None
    action: Optional[str] = None
    observation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    steps: List[ReasoningStep] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(self, "metadata", MappingProxyType(self.metadata))
        # Ensure steps is a tuple or immutable sequence to enforce immutability strictly?
        # Dataclasses with list are mutable. We should convert to tuple or similar.
        # But for now, complying with type signature list but treating as immutable.
        # Ideally: steps: Tuple[ReasoningStep, ...] = field(default_factory=tuple)

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
        """Return a new state with replaced metadata."""
        return replace(self, metadata=metadata)

    def update_metadata(self, updates: Dict[str, Any]) -> "ReActState":
        """Return a new state with updated metadata (merged)."""
        new_metadata = dict(self.metadata)
        new_metadata.update(updates)
        return replace(self, metadata=new_metadata)

    def add_step(self, step: ReasoningStep) -> "ReActState":
        """Return a new state with the step added to history."""
        new_steps = list(self.steps)
        new_steps.append(step)
        return replace(self, steps=new_steps)
