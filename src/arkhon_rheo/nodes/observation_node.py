from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class ObservationNode(BaseNode):
    """
    Node responsible for executing the tool and observing the result.
    """

    def execute(self, state: AgentState) -> AgentState:
        # Stub logic: execute tool 'check_status'
        state["messages"].append({"role": "tool", "content": "Status: OK"})
        return state
