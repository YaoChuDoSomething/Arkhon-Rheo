from arkhon_rheo.core.state import ReActState
from arkhon_rheo.nodes.base import BaseNode


class CommitNode(BaseNode):
    """
    Node responsible for committing the result or state checkpoint.
    """

    def execute(self, state: ReActState) -> ReActState:
        # Stub logic: save to memory/history
        new_meta = dict(state.metadata)
        new_meta["committed"] = True
        return state.with_metadata(new_meta)
