import pytest
import asyncio
from arkhon_rheo.core.subgraph import SubGraph
from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.core.state import ReActState


@pytest.mark.asyncio
async def test_nested_subgraph_execution():
    # Inner Graph
    state = ReActState()
    inner_builder = StateGraph(state)

    def inner_node(s: ReActState) -> ReActState:
        # Avoid NoneType + str error
        thought = s.thought or ""
        return s.with_thought(thought + " -> Inner")

    inner_builder.add_node("inner", inner_node)
    inner_graph = SubGraph("inner_graph", inner_builder, "inner")

    # Outer Graph
    outer_builder = StateGraph(state)

    def outer_start(s: ReActState) -> ReActState:
        return s.with_thought("Outer Start")

    def outer_end(s: ReActState) -> ReActState:
        thought = s.thought or ""
        return s.with_thought(thought + " -> Outer End")

    # To add SubGraph as a node, we might need a wrapper if StateGraph expects specific signature
    # StateGraph expects callable(State) -> State. SubGraph implements __call__.
    # So we can add it directly.

    outer_builder.add_node("start", outer_start)
    outer_builder.add_node("sub", inner_graph.__call__)
    outer_builder.add_node("end", outer_end)

    outer_builder.add_edge("start", "sub")
    outer_builder.add_edge("sub", "end")

    # Run
    # Assuming run() starts execution. But for StateGraph.run(node, max_steps), we need to manually step?
    # Or implement a full run loop.
    # The current StateGraph implementation in test_graph.py seems to have run() and execute_step().
    # Let's verify StateGraph.run() behavior.

    # Based on test_graph.py:
    # final_state = graph.run("A", max_steps=5)
    # It runs loop.

    # So we can run from "start".
    final_state = await outer_builder.run("start", max_steps=10)

    expected_thought = "Outer Start -> Inner -> Outer End"
    assert final_state.thought == expected_thought


@pytest.mark.asyncio
async def test_subgraph_context_propagation():
    # Verify that inner graph sees outer context and can modify it (if shared)
    initial_state = ReActState()
    # Set initial context
    initial_state = initial_state.with_thought("Initial Thought")

    # Inner Graph
    inner_builder = StateGraph(
        ReActState()
    )  # Empty initial state for inner, will get overwritten by call

    def inner_node(s: ReActState) -> ReActState:
        # Check if we can see parent's thought
        parent_thought = s.thought
        return s.with_thought(f"{parent_thought} -> Inner Process")

    inner_builder.add_node("inner", inner_node)
    inner_graph = SubGraph("inner", inner_builder, "inner")

    # Outer Graph
    outer_builder = StateGraph(initial_state)
    outer_builder.add_node("sub", inner_graph.__call__)

    # Run
    final_state = await outer_builder.run("sub")

    # Verify context flow: Initial -> Inner Process
    assert final_state.thought == "Initial Thought -> Inner Process"
