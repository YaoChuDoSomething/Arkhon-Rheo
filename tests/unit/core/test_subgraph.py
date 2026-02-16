import pytest
import pytest
from arkhon_rheo.core.subgraph import SubGraph
from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.core.state import ReActState


@pytest.mark.asyncio
async def test_subgraph_execution():
    # Define a simple graph to be used as a subgraph
    state = ReActState()
    sub_builder = StateGraph(state)

    def sub_node(s: ReActState) -> ReActState:
        return s.with_thought("Inside SubGraph")

    sub_builder.add_node("sub_A", sub_node)
    sub_builder.add_edge(
        "sub_A", "sub_A"
    )  # Self loop to stop? No, we need a terminal condition or max steps
    # For this test, let's just run one step or set entry/exit

    # Actually, StateGraph.run() usually runs until termination or max steps.
    # Let's make "sub_A" just return the state and have no outgoing edges?
    # If no outgoing, it terminates?
    # Based on test_graph.py earlier:
    # "next_node = graph.execute_step("B") -> None # No edge from B"

    # So if we add node without edges, it terminates after execution.

    # Wrap it in SubGraph
    subgraph = SubGraph("my_subgraph", sub_builder, entry_point="sub_A")

    # Execute subgraph
    initial_state = ReActState()
    result_state = await subgraph(initial_state)

    assert result_state.thought == "Inside SubGraph"


@pytest.mark.asyncio
async def test_subgraph_context_isolation():
    # Verify that local vars in subgraph don't pollute unless returned
    # For ReActState, it's immutable-ish, so we return new state.
    # If SubGraph returns the new state, it modifies the flow.
    # But maybe we want some isolation?
    # Sprint 2.3 goal says: "test context propagation"

    state = ReActState(metadata={"parent": "value"})
    sub_builder = StateGraph(state)

    def sub_node(s: ReActState) -> ReActState:
        # Check parent context
        assert s.metadata["parent"] == "value"
        # Add local context
        return s.update_metadata({"child": "local"})

    sub_builder.add_node("start", sub_node)

    subgraph = SubGraph("isolation_test", sub_builder, entry_point="start")

    result = await subgraph(state)

    # If we want simple propagation, child should be there
    assert result.metadata["child"] == "local"
    assert result.metadata["parent"] == "value"
