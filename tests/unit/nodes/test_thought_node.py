from arkhon_rheo.core.state import ReActState
from arkhon_rheo.nodes.thought_node import ThoughtNode


def test_thought_node_execution():
    node = ThoughtNode()
    state = ReActState()

    new_state = node(state)

    assert new_state.thought == "I should check the system status."
    # Ensure other fields are preserved
    assert new_state.action is None
    assert new_state.observation is None


def test_thought_node_prompt_construction():
    # Verify internal logic if needed, accessing private methods for unit testing is common in python
    node = ThoughtNode()
    state = ReActState(action="prev_action")
    prompt = node._construct_prompt(state)
    assert "prev_action" in prompt
