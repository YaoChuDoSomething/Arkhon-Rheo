import pytest
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.action_node import ActionNode
from arkhon_rheo.nodes.observation_node import ObservationNode
from arkhon_rheo.nodes.validate_node import ValidateNode
from arkhon_rheo.nodes.commit_node import CommitNode


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


def test_action_node(base_state):
    node = ActionNode()
    base_state["messages"].append(
        {"role": "assistant", "content": "Need to check status"}
    )
    new_state = node(base_state)
    assert any("Action: check_status()" in m["content"] for m in new_state["messages"])


def test_observation_node(base_state):
    node = ObservationNode()
    base_state["messages"].append(
        {"role": "assistant", "content": "Action: check_status()"}
    )
    new_state = node(base_state)
    assert any("Status: OK" in m["content"] for m in new_state["messages"])


def test_validate_node(base_state):
    node = ValidateNode()
    new_state = node(base_state)
    assert new_state["shared_context"].get("valid") is True


def test_commit_node(base_state):
    node = CommitNode()
    new_state = node(base_state)
    assert new_state["shared_context"].get("committed") is True
