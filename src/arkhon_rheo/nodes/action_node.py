from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class ActionNode(BaseNode):
    """
    Node responsible for determining the action to take.
    """

    def execute(self, state: AgentState) -> AgentState:
        # Stub logic: parse thought to get action
        state["messages"].append(
            {"role": "assistant", "content": "Action: check_status()"}
        )
        return state
