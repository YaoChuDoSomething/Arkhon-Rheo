import pytest
import asyncio
from unittest.mock import MagicMock
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.core.nodes.action_node import ActionNode


@pytest.mark.asyncio
async def test_action_node_execution():
    """Verify ActionNode executes tools and updates messages in AgentState."""

    # Mock tool
    mock_tool = MagicMock()
    mock_tool.run = MagicMock(return_value="File content found.")

    tools = {"read_file": mock_tool}

    node = ActionNode(tools=tools)

    # In the new architecture, we look for tool calls in the last message
    # or a specific format in shared_context/next_step.
    # For this test, let's assume ActionNode extracts tool info from somewhere in state.
    # Current implementation check: ActionNode usually takes a tool_call from the message.

    initial_state: AgentState = {
        "messages": [
            {
                "role": "assistant",
                "content": "I will read the file.",
                "tool_calls": [
                    {
                        "name": "read_file",
                        "args": {"filename": "test.txt"},
                        "id": "call_1",
                    }
                ],
            }
        ],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test",
    }

    new_state = await node(initial_state)

    # Verify tool execution
    assert mock_tool.run.called

    # Verify message update (tool response appended)
    assert len(new_state["messages"]) == 2
    assert new_state["messages"][-1]["role"] == "tool"
    assert new_state["messages"][-1]["content"] == "File content found."


@pytest.mark.asyncio
async def test_action_node_invalid_tool():
    """Verify handling of invalid tools."""
    node = ActionNode(tools={})
    state: AgentState = {
        "messages": [
            {
                "role": "assistant",
                "content": "Use unknown",
                "tool_calls": [{"name": "unknown_tool", "args": {}, "id": "call_2"}],
            }
        ],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test",
    }

    new_state = await node(state)

    assert "Error" in new_state["messages"][-1]["content"]
    assert "unknown_tool" in new_state["messages"][-1]["content"]
