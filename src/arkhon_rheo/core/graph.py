"""Execution Graph Module.

This module provides an advanced execution graph system, allowing for the
definition of nodes, static edges, and conditional routing to manage
agentic workflows.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Union

from arkhon_rheo.core.state import AgentState

# Node function takes AgentState and returns a delta dict or new AgentState (can be async)
NodeAction = Callable[
    [AgentState],
    Union[AgentState, dict[str, Any], Awaitable[Union[AgentState, dict[str, Any]]]],
]


class Graph:
    """An advanced execution graph for managing agentic workflows.

    Supports the registration of logic nodes, static directed edges,
    and conditional branching based on the current state.
    """

    def __init__(self) -> None:
        """Initialize an empty Graph instance."""
        self.nodes: dict[str, NodeAction] = {}
        self.edges: list[tuple[str, str]] = []
        self.conditional_edges: dict[str, dict[str, Any]] = {}

    def add_node(self, name: str, action: NodeAction) -> None:
        """Register a node with a name and action function.

        Args:
            name: Unique identifier for the node.
            action: A callable function or coroutine that processes the state.
        """
        self.nodes[name] = action

    def add_edge(self, start_node: str, end_node: str) -> None:
        """Add a static directed edge from one node to another.

        Args:
            start_node: The name of the source node.
            end_node: The name of the destination node.
        """
        self.edges.append((start_node, end_node))

    def add_conditional_edge(
        self,
        source: str,
        path_map: dict[str, str],
        condition: Callable[[AgentState], str],
    ) -> None:
        """Add a conditional branching edge from a source node.

        The flow is routed based on the result of the condition function.

        Args:
            source: The name of the node to branch from.
            path_map: A mapping from condition results to target node names.
            condition: A function that takes AgentState and returns a key in path_map.
        """
        self.conditional_edges[source] = {"map": path_map, "fn": condition}
