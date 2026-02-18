from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler


class SubGraph:
    """
    A subgraph that encapsulates a Graph and can be executed as a callable node.
    """

    def __init__(self, name: str, graph: Graph, entry_point: str):
        self.name = name
        self.graph = graph
        self.entry_point = entry_point
        self.scheduler = RuntimeScheduler(graph, checkpoint_manager=None)

    async def __call__(self, state: AgentState) -> AgentState:
        """
        Execute the subgraph.
        """
        # Execute the subgraph using the scheduler
        final_state = await self.scheduler.run(state, entry_point=self.entry_point)

        return final_state
