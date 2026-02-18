from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class ValidateNode(BaseNode):
    """
    Node responsible for validating the current state or plan.
    """

    def execute(self, state: AgentState) -> AgentState:
        # Stub logic: validation passes
        state["shared_context"]["valid"] = True
        return state
