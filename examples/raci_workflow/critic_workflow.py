import asyncio
from typing import Any

from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.state import AgentState, RACIAssignment, RACIState
from arkhon_rheo.nodes.governance import DecisionNode, InformNode


async def mock_coder_node(state: AgentState) -> dict[str, Any]:
    return {"messages": [{"role": "assistant", "content": "print('hello world')"}]}


async def mock_qa_node(state: AgentState) -> dict[str, Any]:
    # If already approved by architect in a previous loop, don't overwrite
    if state.get("shared_context", {}).get("verdict") == "approved":
        return {}
    # Force a rejection for the first pass
    return {"shared_context": {"verdict": "rejected"}}


async def main():
    # 1. Define RACI Config
    raci_config = {
        "coding_task": RACIAssignment(
            responsible=["CoderAgent", "QAAgent"],
            accountable="ArchitectAgent",
            consulted=[],
            informed=["PMAgent"],
        )
    }

    # 2. Setup Graph
    workflow = Graph()

    workflow.add_node("Coder", mock_coder_node)
    workflow.add_node("QA_Review", mock_qa_node)
    # DecisionNode uses current_task to determine backtrack target
    workflow.add_node(
        "Governance", DecisionNode(accountable_agent_name="ArchitectAgent")
    )
    workflow.add_node("Notify", InformNode())

    workflow.add_edge("Coder", "QA_Review")
    workflow.add_edge("QA_Review", "Governance")

    state: RACIState = {
        "messages": [],
        "next_step": "Coder",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_raci_1",
        "raci_config": raci_config,
        "current_task": "coding_task",
    }


    current_node = "Coder"

    # We simulate exactly 5 steps to show the loop:
    # Coder -> QA -> Governance (Reject) -> Coder -> QA -> Governance (Approve) -> Notify -> END
    for _i in range(10):
        if current_node == "END":
            break

        node_fn = workflow.nodes.get(current_node)
        if not node_fn:
            break

        # Execute node and merge results into state
        result = await node_fn(state)
        if result:
            state.update(result)

        # Determine next node based on manual flow logic for this simulation
        if current_node == "Coder":
            current_node = "QA_Review"
        elif current_node == "QA_Review":
            current_node = "Governance"
        elif current_node == "Governance":
            next_step = state.get("next_step")
            if next_step == "coding_task":  # Backtrack to responsible node
                current_node = "Coder"
                # For simulation purposes, we "fix" the issue so the next pass succeeds
                state["shared_context"]["verdict"] = "approved"
            else:
                current_node = "Notify"
        elif current_node == "Notify":
            current_node = "END"



if __name__ == "__main__":
    asyncio.run(main())
