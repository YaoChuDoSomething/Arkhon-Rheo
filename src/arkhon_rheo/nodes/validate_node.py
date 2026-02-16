from arkhon_rheo.core.state import ReActState
from arkhon_rheo.nodes.base import BaseNode


class ValidateNode(BaseNode):
    """
    Node responsible for validating the current state or plan.
    """

    def execute(self, state: ReActState) -> ReActState:
        # Stub logic: validation passes
        # Creates a new thought or metadata update indicating success
        # For now, just pass through or add metadata
        new_meta = dict(state.metadata)
        new_meta["valid"] = True
        return state.with_metadata(new_meta)
