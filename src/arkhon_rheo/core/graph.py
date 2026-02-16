from typing import Callable, Dict, List, Optional, Any, Union
from arkhon_rheo.core.state import AgentState

# Node function takes AgentState and returns a delta Dict or new AgentState
NodeAction = Callable[[AgentState], Union[AgentState, Dict[str, Any]]]


class Graph:
    """
    An advanced execution graph inspired by LangGraph.
    Supports nodes, static edges, and conditional routing.
    """

    def __init__(self):
        self.nodes: Dict[str, NodeAction] = {}
        self.edges: List[tuple] = []
        self.conditional_edges: Dict[str, Dict[str, Any]] = {}

    def add_node(self, name: str, action: NodeAction):
        """Register a node with a name and action function."""
        self.nodes[name] = action

    def add_edge(self, start_node: str, end_node: str):
        """Add a static directed edge from start_node to end_node."""
        self.edges.append((start_node, end_node))

    def add_conditional_edge(
        self, source: str, path_map: Dict[str, str], condition: Callable[[AgentState], str]
    ):
        """
        Routes the flow from a source node based on the result of a condition function.

        Args:
            source: The node to branch from.
            path_map: A mapping from condition results to target node names.
            condition: A function that takes AgentState and returns a key in path_map.
        """
        self.conditional_edges[source] = {"map": path_map, "fn": condition}
