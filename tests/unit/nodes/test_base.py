import pytest
from arkhon_rheo.core.state import ReActState
from arkhon_rheo.nodes.base import BaseNode


class MockNode(BaseNode):
    def execute(self, state: ReActState) -> ReActState:
        return state.with_thought("Mock executed")


def test_base_node_execution():
    node = MockNode()
    state = ReActState()
    new_state = node(state)
    assert new_state.thought == "Mock executed"


def test_base_node_lifecycle(capsys):
    # We can't easily test logging with capsys without configuring logging to stdout/stderr
    # But we can verify the method is called.
    # Alternatively, we can mock the hooks in a subclass

    hooks_called = []

    class HookedNode(BaseNode):
        def before_execute(self, state: ReActState) -> None:
            hooks_called.append("before")

        def execute(self, state: ReActState) -> ReActState:
            hooks_called.append("execute")
            return state

        def after_execute(self, state: ReActState) -> None:
            hooks_called.append("after")

    node = HookedNode()
    node(ReActState())

    assert hooks_called == ["before", "execute", "after"]


def test_abstract_method_enforcement():
    with pytest.raises(TypeError):
        # Should raise TypeError because execute is abstract
        class IncompleteNode(BaseNode):
            pass

        IncompleteNode()
