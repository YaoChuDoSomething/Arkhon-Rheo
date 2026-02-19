from unittest.mock import MagicMock

import pytest

from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.action_node import ActionNode
from arkhon_rheo.nodes.commit_node import CommitNode
from arkhon_rheo.nodes.observation_node import ObservationNode
from arkhon_rheo.nodes.thought_node import ThoughtNode
from arkhon_rheo.nodes.validate_node import ValidateNode


@pytest.mark.asyncio
async def test_full_react_cycle():
    # 1. Initialize State and Graph
    initial_state: AgentState = {
        "messages": [],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_thread",
    }
    graph = Graph()

    # Mock LLM
    mock_llm = MagicMock()
    # First thought: check status
    # Second thought: status is OK, valid, commit
    # But this test is linear linear cycle (Thought -> Action -> Obs -> Val -> Commit -> End)
    # ThoughtNode: "I needs to check system status."
    # ActionNode: "Action: check_status()" - wait, ActionNode logic parses tool calls.
    # The integration test expects "Action: check_status()" in content.
    # Currently ActionNode executes tool calls from last message.
    # ThoughtNode generates content.
    # We need ThoughtNode to generate a message with tool_calls for ActionNode to pick up.

    # Let's see what the test expects:
    # assert "check the system status" in initial_state["messages"]
    # assert "Action: check_status()" in initial_state["messages"] (This seems like old ActionNode stub logic?)

    # Wait, the new ActionNode executes tool calls. It doesn't output "Action: check_status()".
    # It outputs "role": "tool", "content": "Tool Result".
    # The old ActionNode stub output "Action: check_status()".

    # If I replaced ActionNode implementation with the core one, the behavior changed!
    # The integration test relies on OLD behavior ("Action: check_status()").
    # This means the integration test is testing the STUB behavior.
    # Now that I unified to the REAL behavior, I need to update the test or make sure the real behavior satisfies it.

    # REAL Behavior:
    # ThoughtNode -> produces message with tool_calls.
    # ActionNode -> executes tool_calls -> produces tool message.

    # The test assertions:
    # assert any("Action: check_status()" in m["content"] ...)

    # This assertion will FAIL with new ActionNode.
    # I should update the test to expect correct behavior.

    # Also ThoughtNode needs to produce tool_calls.
    # Mock LLM needs to return AIMessage with tool_calls.

    # Mocking:
    mock_msg = MagicMock()
    mock_msg.content = "I need to check the system status."
    mock_msg.tool_calls = [{"name": "check_status", "args": {}, "id": "call_1"}]
    mock_llm.invoke.return_value = mock_msg

    mock_tool = MagicMock()
    mock_tool.run.return_value = "Status: OK"
    tools = {"check_status": mock_tool}

    # 2. Add Nodes
    graph.add_node("thought", ThoughtNode(llm=mock_llm))
    graph.add_node("action", ActionNode(tools=tools))
    graph.add_node("observation", ObservationNode())
    graph.add_node("validate", ValidateNode())
    graph.add_node("commit", CommitNode())

    # 3. Add Edges (Linear cycle for this test)
    # Thought -> Action -> Observation -> Validate -> Commit
    graph.add_edge("thought", "action")
    graph.add_edge("action", "observation")
    graph.add_edge("observation", "validate")
    graph.add_edge("validate", "commit")
    graph.add_edge("commit", "__end__")

    # 4. Run using RuntimeScheduler
    scheduler = RuntimeScheduler(graph, checkpoint_manager=None)
    await scheduler.run(initial_state, "thought")

    # 5. Verify Final State
    # Note: messages are appended
    assert any(
        "check the system status" in m["content"] for m in initial_state["messages"]
    )
    # New ActionNode appends tool message with content from tool run
    # assert any("Status: OK" in m["content"] for m in initial_state["messages"])
    # Wait, check valid assertion:
    # The tool result "Status: OK" should be in a message with role tool.
    tool_messages = [m for m in initial_state["messages"] if m.get("role") == "tool"]
    assert any("Status: OK" in m["content"] for m in tool_messages)
    assert initial_state["shared_context"].get("valid") is True
    assert initial_state["shared_context"].get("committed") is True
