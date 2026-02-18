import pytest
import asyncio
from arkhon_rheo.core.subgraph import SubGraph
from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler


@pytest.fixture
def initial_state():
    return {
        "messages": [],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_thread",
    }


@pytest.mark.asyncio
async def test_nested_subgraph_execution(initial_state):
    # Inner Graph
    inner_graph_obj = Graph()

    async def inner_node(s: AgentState) -> AgentState:
        last_msg = s["messages"][-1]["content"] if s["messages"] else ""
        s["messages"].append({"role": "assistant", "content": last_msg + " -> Inner"})
        return s

    inner_graph_obj.add_node("inner", inner_node)
    inner_graph_obj.add_edge("inner", "__end__")

    inner_subgraph = SubGraph("inner_graph", inner_graph_obj, "inner")

    # Outer Graph
    outer_graph_obj = Graph()

    async def outer_start(s: AgentState) -> AgentState:
        s["messages"].append({"role": "assistant", "content": "Outer Start"})
        return s

    async def outer_end(s: AgentState) -> AgentState:
        last_msg = s["messages"][-1]["content"] if s["messages"] else ""
        s["messages"].append(
            {"role": "assistant", "content": last_msg + " -> Outer End"}
        )
        s["is_completed"] = True
        return s

    outer_graph_obj.add_node("start", outer_start)
    outer_graph_obj.add_node("sub", inner_subgraph)
    outer_graph_obj.add_node("end", outer_end)

    outer_graph_obj.add_edge("start", "sub")
    outer_graph_obj.add_edge("sub", "end")

    # Run using scheduler
    scheduler = RuntimeScheduler(outer_graph_obj, checkpoint_manager=None)
    await scheduler.run(initial_state, "start")

    expected_content = "Outer Start -> Inner -> Outer End"
    assert initial_state["messages"][-1]["content"] == expected_content


@pytest.mark.asyncio
async def test_subgraph_context_propagation(initial_state):
    # Verify that inner graph sees outer context and can modify it (if shared)
    initial_state["messages"].append(
        {"role": "assistant", "content": "Initial Thought"}
    )

    # Inner Graph
    inner_graph_obj = Graph()

    async def inner_node(s: AgentState) -> AgentState:
        # Check if we can see parent's thought in messages
        parent_thought = s["messages"][-1]["content"]
        s["messages"].append(
            {"role": "assistant", "content": f"{parent_thought} -> Inner Process"}
        )
        return s

    inner_graph_obj.add_node("inner", inner_node)
    inner_graph_obj.add_edge("inner", "__end__")
    inner_subgraph = SubGraph("inner", inner_graph_obj, "inner")

    # Outer Graph
    outer_graph_obj = Graph()
    outer_graph_obj.add_node("sub", inner_subgraph)
    outer_graph_obj.add_edge("sub", "__end__")

    # Run
    scheduler = RuntimeScheduler(outer_graph_obj, checkpoint_manager=None)
    await scheduler.run(initial_state, "sub")

    # Verify context flow: Initial -> Inner Process
    assert (
        initial_state["messages"][-1]["content"] == "Initial Thought -> Inner Process"
    )
