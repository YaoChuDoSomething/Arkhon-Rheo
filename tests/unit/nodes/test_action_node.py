import pytest
from unittest.mock import MagicMock
from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.nodes.action_node import ActionNode


def test_action_node_execution():
    """Verify ActionNode executes tools and updates observation."""

    # Mock tool registry or mapping
    mock_tool = MagicMock()
    mock_tool.run.return_value = "File content found."

    tools = {"read_file": mock_tool}

    node = ActionNode(tools=tools)

    # State with an action pending
    # Assuming action format: "tool_name: input" or JSON
    # For MVP simplicity, let's use "tool_name:input" string parsing
    initial_state = ReActState(action="read_file:test.txt")

    new_state = node(initial_state)

    # Verify tool execution
    mock_tool.run.assert_called_with("test.txt")

    # Verify observation update
    assert new_state.observation == "File content found."
    assert new_state.action is None  # Action should be cleared or marked done?
    # Usually in ReAct, action stays until next thought clears it?
    # Or we keep history in steps. Let's assume action field is current pending action.


def test_action_node_invalid_tool():
    """Verify handling of invalid tools."""
    node = ActionNode(tools={})
    state = ReActState(action="unknown_tool:argument")

    new_state = node(state)

    assert "Error: Tool 'unknown_tool' not found" in new_state.observation
