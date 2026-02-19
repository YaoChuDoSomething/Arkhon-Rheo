import pytest

from arkhon_rheo.nodes.action_node import ActionNode
from arkhon_rheo.nodes.commit_node import CommitNode
from arkhon_rheo.nodes.observation_node import ObservationNode
from arkhon_rheo.nodes.validate_node import ValidateNode


@pytest.fixture
def base_state():
    return {
        "messages": [],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test",
    }


@pytest.mark.asyncio
async def test_action_node(base_state):
    # Mock behavior for new ActionNode
    # ActionNode expects tools dict
    node = ActionNode(tools={})
    # ActionNode expects last message to have tool_calls
    base_state["messages"].append(
        {
            "role": "assistant",
            "content": "Checking status",
            "tool_calls": [{"name": "check_status", "args": {}, "id": "1"}],
        }
    )

    # With empty tools, it should error
    new_state = await node(base_state)
    assert any(
        "Error: Tool 'check_status' not found" in m["content"]
        for m in new_state["messages"]
    )


@pytest.mark.asyncio
async def test_observation_node(base_state):
    node = ObservationNode()
    # ObservationNode probably expects "Action: ..." format if it's the old stub?
    # Or does it read tool output?
    # Let's assume old behavior for ObservationNode if I haven't changed it.
    base_state["messages"].append(
        {"role": "assistant", "content": "Action: check_status()"}
    )
    new_state = await node(base_state)
    assert any("Status: OK" in m["content"] for m in new_state["messages"])


@pytest.mark.asyncio
async def test_validate_node(base_state):
    node = ValidateNode()
    new_state = await node(base_state)
    assert new_state["shared_context"].get("valid") is True


@pytest.mark.asyncio
async def test_commit_node(base_state):
    node = CommitNode()
    new_state = await node(base_state)
    assert new_state["shared_context"].get("committed") is True
