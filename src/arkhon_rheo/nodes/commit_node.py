from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class CommitNode(BaseNode):
    """
    Node responsible for committing the result or state checkpoint.
    """

    def execute(self, state: AgentState) -> AgentState:
        # Stub logic: save to memory/history
        state["shared_context"]["committed"] = True
        return state
