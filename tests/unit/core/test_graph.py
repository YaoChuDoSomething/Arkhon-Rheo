import pytest

from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler
from arkhon_rheo.core.state import AgentState


@pytest.fixture
def initial_state():
    return {
        "messages": [],
        "next_step": "start",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_thread",
    }


@pytest.mark.asyncio
async def test_graph_and_scheduler_flow(initial_state):
    graph = Graph()

    def node_a(state: AgentState):
        return {"messages": [{"role": "assistant", "content": "Thought A"}]}

    def node_b(state: AgentState):
        return {
            "messages": [{"role": "assistant", "content": "Action B"}],
            "is_completed": True,
        }

    graph.add_node("A", node_a)
    graph.add_node("B", node_b)
    graph.add_edge("A", "B")

    scheduler = RuntimeScheduler(graph, checkpoint_manager=None)
    await scheduler.run(initial_state, "A")

    assert len(initial_state["messages"]) == 2
    assert initial_state["messages"][0]["content"] == "Thought A"
    assert initial_state["messages"][1]["content"] == "Action B"
    assert initial_state["is_completed"] is True


@pytest.mark.asyncio
async def test_conditional_routing(initial_state):
    graph = Graph()

    def logic_node(state: AgentState):
        state["shared_context"]["val"] = 10
        return state

    def end_node(state: AgentState):
        state["is_completed"] = True
        return state

    def condition_fn(state: AgentState):
        return "yes" if state["shared_context"].get("val") == 10 else "no"

    graph.add_node("logic", logic_node)
    graph.add_node("end", end_node)

    graph.add_conditional_edge(
        source="logic", path_map={"yes": "end", "no": "END"}, condition=condition_fn
    )

    scheduler = RuntimeScheduler(graph, checkpoint_manager=None)
    await scheduler.run(initial_state, "logic")

    assert initial_state["shared_context"]["val"] == 10
    assert initial_state["is_completed"] is True
