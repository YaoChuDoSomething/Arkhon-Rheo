from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.core.state import ReActState


class SubGraph:
    """
    A subgraph that encapsulates a StateGraph and can be executed as a callable node.
    """

    def __init__(self, name: str, graph: StateGraph, entry_point: str):
        self.name = name
        self.graph = graph
        self.entry_point = entry_point

    async def __call__(self, state: ReActState) -> ReActState:
        """
        Execute the subgraph.
        """
        # Set the current state of the internal graph to the provided state
        # to ensure context propagation (like previous thoughts)
        self.graph._current_state = state

        final_state = await self.graph.run(
            self.entry_point, max_steps=10
        )  # Default max steps for subgraphs

        return final_state
