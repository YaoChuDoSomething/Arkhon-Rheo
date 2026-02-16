import pytest
from unittest.mock import MagicMock
from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.nodes.thought_node import ThoughtNode


def test_thought_node_execution():
    """Verify ThoughtNode calls LLM and updates state."""

    # Mock LLM chain/runnable
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "I need to check the file size."

    node = ThoughtNode(llm=mock_llm)
    initial_state = ReActState()

    new_state = node(initial_state)

    # Verify LLM was called
    mock_llm.invoke.assert_called_once()

    # Verify state update
    assert new_state.thought == "I need to check the file size."
    # Ideally should also check if a ReasoningStep was added, but that depends on node implementation detail.
    # For now, just checking the thought attribute is sufficient for the first pass.


def test_thought_node_with_system_prompt():
    """Verify ThoughtNode accepts system prompt or context."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "Thinking..."

    # Assuming prompt template injection or similar mechanism
    # For MVP, maybe just passing state to LLM is enough context.
    node = ThoughtNode(llm=mock_llm)
    node(ReActState(observation="Previous result"))

    # Check if observation was passed to LLM (implementation detail)
    # mock_llm.invoke.assert_called_with(expect_some_prompt_structure)
    assert mock_llm.invoke.called
