from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.graph import StateGraph
import pytest


@pytest.mark.asyncio
async def test_graph_initialization():
    state = ReActState()
    graph = StateGraph(state)
    assert graph.current_state == state


@pytest.mark.asyncio
async def test_graph_execution_flow():
    initial_state = ReActState()
    graph = StateGraph(initial_state)

    def node_a(state: ReActState) -> ReActState:
        return state.with_thought("Thought from A")

    def node_b(state: ReActState) -> ReActState:
        return state.with_action("Action from B")

    graph.add_node("A", node_a)
    graph.add_node("B", node_b)
    graph.add_edge("A", "B")

    # Run step by step
    # Note: execute_step might return the next node ID or the new state?
    # Based on ReAct pattern, often we run until termination.
    # But for now let's assume granular control: execute_step(node_id) -> next_node_id
    next_node = await graph.execute_step("A")
    assert next_node == "B"
    assert graph.current_state.thought == "Thought from A"
    assert graph.current_state.action is None

    next_node = await graph.execute_step("B")
    assert next_node is None  # No edge from B
    assert graph.current_state.action == "Action from B"


@pytest.mark.asyncio
async def test_graph_run_loop():
    initial_state = ReActState()
    graph = StateGraph(initial_state)

    def node_a(state: ReActState) -> ReActState:
        count = state.metadata.get("count", 0)
        return state.with_metadata({"count": count + 1})

    graph.add_node("A", node_a)
    # Self loop for testing max steps
    graph.add_edge("A", "A")

    # This should run A 5 times and stop
    final_state = await graph.run("A", max_steps=5)
    assert final_state.metadata["count"] == 5
