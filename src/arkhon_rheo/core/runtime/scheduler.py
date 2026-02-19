"""Runtime Scheduler Module.

This module provides the RuntimeScheduler class, which serves as the
asynchronous execution engine for agentic graphs, managing node transitions
and state persistence.
"""

from __future__ import annotations

import asyncio
from typing import Any

from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.state import AgentState


class RuntimeScheduler:
    """Asynchronous executor for the agentic graph.

    The scheduler manages the progression of the graph by executing nodes
    one by one, applying state changes, and determining the next node to
    execute based on static or conditional edges.

    Attributes:
        graph: The Graph instance containing the nodes and edges to execute.
        checkpoint_manager: An optional manager for high-security checkpointing.
    """

    def __init__(self, graph: Graph, checkpoint_manager: Any) -> None:
        """Initialize a RuntimeScheduler instance.

        Args:
            graph: The execution graph.
            checkpoint_manager: Manager for state persistence.
        """
        self.graph = graph
        self.checkpoint_manager = checkpoint_manager

    async def step(self, current_node: str, state: AgentState) -> str:
        """Execute a single node and determine the next transition.

        Args:
            current_node: The name of the node to execute.
            state: The current AgentState.

        Returns:
            The name of the next node to execute, or "END" to terminate.
        """
        if current_node not in self.graph.nodes:
            return "END"

        try:
            result = await self._execute_node(current_node, state)
            if result:
                self._apply_delta(state, result)
        except Exception as e:
            return self._handle_error(state, e)

        self._save_checkpoint(state)
        return self._resolve_next(current_node, state)

    async def _execute_node(
        self, node_name: str, state: AgentState
    ) -> dict[str, Any] | None:
        """Execute a specific node's action."""
        action = self.graph.nodes[node_name]
        result = action(state)
        if asyncio.iscoroutine(result):
            result = await result
        return result if isinstance(result, dict) else None

    def _apply_delta(self, state: AgentState, result: dict[str, Any]) -> None:
        """Apply the results of a node execution to the state."""
        for k, v in result.items():
            if k == "messages" and k in state:
                state[k] = state[k] + v
            else:
                state[k] = v

    def _handle_error(self, state: AgentState, error: Exception) -> str:
        """Log execution errors and terminate the graph flow."""
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(str(error))
        return "END"

    def _save_checkpoint(self, state: AgentState) -> None:
        """Persist the current state if a checkpoint manager is available."""
        if self.checkpoint_manager:
            self.checkpoint_manager.save_checkpoint(state)

    def _resolve_next(self, current_node: str, state: AgentState) -> str:
        """Determine the next node based on graph topology or state-based logic."""
        # Conditional Edges
        if current_node in self.graph.conditional_edges:
            cond_cfg = self.graph.conditional_edges[current_node]
            decision = cond_cfg["fn"](state)
            return cond_cfg["map"].get(decision, "END")

        # Static Edges
        for start, end in self.graph.edges:
            if start == current_node:
                return end

        return "END"

    async def run(self, initial_state: AgentState, entry_point: str) -> AgentState:
        """Main control loop for the execution engine.

        Continues executing steps until an "END" node is reached or
        the state is marked as completed.

        Args:
            initial_state: The starting state for the graph.
            entry_point: The name of the first node to execute.

        Returns:
            The final AgentState after execution finishes.
        """
        curr = entry_point
        while curr != "END" and not initial_state.get("is_completed"):
            curr = await self.step(curr, initial_state)
        return initial_state
