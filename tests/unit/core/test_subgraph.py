import pytest

from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler
from arkhon_rheo.core.state import AgentState


@pytest.mark.asyncio
async def test_graph_as_subgraph_execution():
    """Test that a Graph can be executed and its result returned to another context."""
    # Define a 'subgraph'
    sub_graph = Graph()

    async def sub_node_a(state: AgentState) -> AgentState:
        state["shared_context"]["sub"] = "completed"
        return state

    sub_graph.add_node("start", sub_node_a)
    sub_graph.add_edge("start", "__end__")

    # Initial state
    initial_state: AgentState = {
        "messages": [],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_thread",
    }

    # Execute it using the scheduler
    scheduler = RuntimeScheduler(sub_graph, checkpoint_manager=None)
    final_state = await scheduler.run(initial_state, entry_point="start")

    assert final_state["shared_context"]["sub"] == "completed"


@pytest.mark.asyncio
async def test_subgraph_context_propagation():
    """Verify that context is correctly passed between nested execution flows."""
    parent_state: AgentState = {
        "messages": [],
        "next_step": "",
        "shared_context": {"parent": "data"},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_thread",
    }

    child_graph = Graph()

    async def child_node(state: AgentState) -> AgentState:
        assert state["shared_context"]["parent"] == "data"
        state["shared_context"]["child"] = "updated"
        return state

    child_graph.add_node("child_start", child_node)
    child_graph.add_edge("child_start", "__end__")

    scheduler = RuntimeScheduler(child_graph, checkpoint_manager=None)
    result = await scheduler.run(parent_state, entry_point="child_start")

    assert result["shared_context"]["child"] == "updated"
    assert result["shared_context"]["parent"] == "data"
