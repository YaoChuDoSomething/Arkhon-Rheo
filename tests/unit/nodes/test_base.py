import pytest
from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.nodes.base import BaseNode


def test_base_node_abstract_method():
    """Verify that BaseNode cannot be instantiated directly."""
    # It should not be possible to instantiate an abstract base class
    # But usually calling `BaseNode()` fails or `execute` raises NotImplementedError depending on implementation.
    # We prefer ABC meta.

    with pytest.raises(TypeError):
        BaseNode()


def test_concrete_node_implementation():
    """Verify a concrete implementation works."""

    class TestNode(BaseNode):
        def execute(self, state: ReActState) -> ReActState:
            return state.with_thought("Executed")

    node = TestNode()
    initial_state = ReActState()
    new_state = node(initial_state)  # Should be callable
    assert new_state.thought == "Executed"
