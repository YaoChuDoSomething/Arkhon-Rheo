import pytest

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


def test_base_node_abstract_method():
    """Verify that BaseNode cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseNode()


def test_concrete_node_implementation():
    """Verify a concrete implementation works with AgentState."""

    class TestNode(BaseNode):
        async def execute(self, state: AgentState) -> AgentState:
            state["shared_context"]["executed"] = True
            return state

    node = TestNode()
    initial_state: AgentState = {
        "messages": [],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test",
    }

    # BaseNode makes the class callable, invoking execute
    import asyncio

    new_state = asyncio.run(node(initial_state))
    assert new_state["shared_context"]["executed"] is True
