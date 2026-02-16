from arkhon_rheo.core.state import ReActState
from arkhon_rheo.nodes.action_node import ActionNode
from arkhon_rheo.nodes.observation_node import ObservationNode
from arkhon_rheo.nodes.validate_node import ValidateNode
from arkhon_rheo.nodes.commit_node import CommitNode


def test_action_node():
    node = ActionNode()
    state = ReActState(thought="Need to check status")
    new_state = node(state)
    assert new_state.action == "check_status()"


def test_observation_node():
    node = ObservationNode()
    state = ReActState(action="check_status()")
    new_state = node(state)
    assert new_state.observation == "Status: OK"


def test_validate_node():
    node = ValidateNode()
    state = ReActState(thought="Plan A")
    new_state = node(state)
    assert new_state.metadata.get("valid") is True


def test_commit_node():
    node = CommitNode()
    state = ReActState(observation="Done")
    new_state = node(state)
    assert new_state.metadata.get("committed") is True
