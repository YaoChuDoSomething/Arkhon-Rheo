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
