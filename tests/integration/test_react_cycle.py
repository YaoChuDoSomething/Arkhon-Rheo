import pytest
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler
from arkhon_rheo.nodes.thought_node import ThoughtNode
from arkhon_rheo.nodes.action_node import ActionNode
from arkhon_rheo.nodes.observation_node import ObservationNode
from arkhon_rheo.nodes.validate_node import ValidateNode
from arkhon_rheo.nodes.commit_node import CommitNode


@pytest.mark.asyncio
async def test_full_react_cycle():
    # 1. Initialize State and Graph
    initial_state: AgentState = {
        "messages": [],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_thread",
    }
    graph = Graph()

    # 2. Add Nodes
    graph.add_node("thought", ThoughtNode())
    graph.add_node("action", ActionNode())
    graph.add_node("observation", ObservationNode())
    graph.add_node("validate", ValidateNode())
    graph.add_node("commit", CommitNode())

    # 3. Add Edges (Linear cycle for this test)
    # Thought -> Action -> Observation -> Validate -> Commit
    graph.add_edge("thought", "action")
    graph.add_edge("action", "observation")
    graph.add_edge("observation", "validate")
    graph.add_edge("validate", "commit")
    graph.add_edge("commit", "__end__")

    # 4. Run using RuntimeScheduler
    scheduler = RuntimeScheduler(graph, checkpoint_manager=None)
    await scheduler.run(initial_state, "thought")

    # 5. Verify Final State
    # Note: messages are appended
    assert any(
        "check the system status" in m["content"] for m in initial_state["messages"]
    )
    assert any(
        "Action: check_status()" in m["content"] for m in initial_state["messages"]
    )
    assert any("Status: OK" in m["content"] for m in initial_state["messages"])
    assert initial_state["shared_context"].get("valid") is True
    assert initial_state["shared_context"].get("committed") is True
