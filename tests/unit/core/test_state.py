import pytest
from arkhon_rheo.core.state import ReActState


def test_react_state_immutability():
    """Test that ReActState is immutable."""
    state = ReActState(
        thought="Initial thought",
        action="Initial action",
        observation="Initial observation",
        metadata={"key": "value"},
    )

    with pytest.raises(AttributeError):
        state.thought = "New thought"  # type: ignore[misc]

    with pytest.raises(TypeError):
        state.metadata["key"] = "new value"


def test_react_state_initialization():
    """Test standard initialization."""
    state = ReActState(
        thought="Thinking...",
        action="Action...",
        observation="Result...",
        metadata={"step": 1},
    )

    assert state.thought == "Thinking..."
    assert state.action == "Action..."
    assert state.observation == "Result..."
    assert state.metadata == {"step": 1}


def test_react_state_defaults():
    """Test default values."""
    state = ReActState()
    assert state.thought is None
    assert state.action is None
    assert state.observation is None
    assert state.metadata == {}


def test_react_state_transitions():
    """Test state transition methods (with_*)."""
    state = ReActState()

    new_state = state.with_thought("New thought")
    assert new_state.thought == "New thought"
    assert new_state.action is None  # Others should remain unchanged
    assert state.thought is None  # Original should remain unchanged

    new_state_2 = new_state.with_action("New action")
    assert new_state_2.thought == "New thought"
    assert new_state_2.action == "New action"

    new_state_3 = new_state_2.with_observation("New result")
    assert new_state_3.observation == "New result"

    new_state_4 = new_state_3.with_metadata({"new": "meta"})
    assert new_state_4.metadata == {"new": "meta"}


def test_reasoning_step_creation():
    """Test ReasoningStep creation and immutability."""
    # This should fail initially as ReasoningStep is not defined
    from arkhon_rheo.core.state import ReasoningStep

    step = ReasoningStep(
        step_id="step-1",
        type="thought",
        content="Thinking about...",
        timestamp=1234567890.0,
    )
    assert step.step_id == "step-1"
    assert step.type == "thought"

    with pytest.raises(AttributeError):
        step.content = "New content"  # type: ignore


def test_react_state_with_steps():
    """Test ReActState handling of steps."""
    from arkhon_rheo.core.state import ReActState, ReasoningStep

    step = ReasoningStep(
        step_id="step-1",
        type="thought",
        content="Thinking...",
        timestamp=1234567890.0,
    )

    state = ReActState()
    # Assuming we add a method to add steps or pass them in init
    # For now, let's test init with steps if we plan to add it
    # or a method like add_step returning new state

    # Check if steps attribute exists (it shouldn't yet in current code)
    # This assert is to drive the implementation
    assert hasattr(state, "steps")
    assert state.steps == []

    new_state = state.add_step(step)
    assert len(new_state.steps) == 1
    assert new_state.steps[0] == step
