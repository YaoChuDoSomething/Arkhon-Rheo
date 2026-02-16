from arkhon_rheo.core.state import ReActState
from arkhon_rheo.nodes.base import BaseNode


class ObservationNode(BaseNode):
    """
    Node responsible for executing the tool and observing the result.
    """

    def execute(self, state: ReActState) -> ReActState:
        # Stub logic: execute tool 'check_status'
        return state.with_observation("Status: OK")
