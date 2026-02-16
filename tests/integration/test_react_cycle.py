from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.nodes.thought_node import ThoughtNode
from arkhon_rheo.nodes.action_node import ActionNode
from arkhon_rheo.nodes.observation_node import ObservationNode
from arkhon_rheo.nodes.validate_node import ValidateNode
from arkhon_rheo.nodes.commit_node import CommitNode


def test_full_react_cycle():
    # 1. Initialize State and Graph
    initial_state = ReActState()
    graph = StateGraph(initial_state)

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
    # Commit is end node

    # 4. Run
    final_state = graph.run("thought")

    # 5. Verify Final State
    assert final_state.thought == "I should check the system status."
    assert final_state.action == "check_status()"
    assert final_state.observation == "Status: OK"
    assert final_state.metadata.get("valid") is True
    assert final_state.metadata.get("committed") is True
