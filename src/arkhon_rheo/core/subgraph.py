"""Subgraph Module.

This module provides the SubGraph class, which allows a Graph instance to
be encapsulated and executed as a single callable node within another Graph.
"""

from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler
from arkhon_rheo.core.state import AgentState


class SubGraph:
    """A subgraph that encapsulates a Graph and can be executed as a node.

    This allows for hierarchical graph structures and reuse of complex
    logic components.

    Attributes:
        name: Unique identifier for the subgraph.
        graph: The Graph instance to be executed.
        entry_point: The name of the node where execution starts.
        scheduler: The runtime scheduler used to manage subgraph execution.
    """

    def __init__(self, name: str, graph: Graph, entry_point: str) -> None:
        """Initialize a SubGraph instance.

        Args:
            name: The name of the subgraph.
            graph: The Graph instance to encapsulate.
            entry_point: The node name to start execution from.
        """
        self.name = name
        self.graph = graph
        self.entry_point = entry_point
        self.scheduler = RuntimeScheduler(graph, checkpoint_manager=None)

    async def __call__(self, state: AgentState) -> AgentState:
        """Execute the encapsulated subgraph with the provided state.

        Args:
            state: The input state for the subgraph.

        Returns:
            The final state after subgraph execution.
        """
        # Execute the subgraph using the scheduler
        return await self.scheduler.run(state, entry_point=self.entry_point)

