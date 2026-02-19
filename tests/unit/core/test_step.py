from datetime import datetime

from arkhon_rheo.core.step import ReActStep, StepType


def test_step_initialization():
    """Test ReActStep initialization."""
    step = ReActStep(
        step_type=StepType.THOUGHT,
        content="Thinking process...",
        timestamp=datetime.now(),
    )
    assert step.step_type == StepType.THOUGHT
    assert step.content == "Thinking process..."
    assert isinstance(step.timestamp, datetime)


def test_step_serialization():
    """Test converting step to dict/json."""
    timestamp = datetime.now()
    step = ReActStep(step_type=StepType.ACTION, content="tool_call(arg=1)", timestamp=timestamp)

    data = step.to_dict()
    assert data["step_type"] == "action"
    assert data["content"] == "tool_call(arg=1)"
    assert data["timestamp"] == timestamp.isoformat()


def test_step_deserialization():
    """Test creating step from dict."""
    timestamp_str = "2023-10-27T10:00:00"
    data = {
        "step_type": "observation",
        "content": "Result: 42",
        "timestamp": timestamp_str,
    }

    step = ReActStep.from_dict(data)
    assert step.step_type == StepType.OBSERVATION
    assert step.content == "Result: 42"
    assert step.timestamp.isoformat() == timestamp_str


def test_step_types():
    """Test all step types are available."""
    assert StepType.THOUGHT == "thought"
    assert StepType.ACTION == "action"
    assert StepType.OBSERVATION == "observation"
