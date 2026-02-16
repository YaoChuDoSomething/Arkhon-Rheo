from arkhon_rheo.core.state import ReActState
from arkhon_rheo.nodes.base import BaseNode


class ActionNode(BaseNode):
    """
    Node responsible for determining the action to take.
    """

    def execute(self, state: ReActState) -> ReActState:
        # Stub logic: parse thought to get action
        return state.with_action("check_status()")
