"""Observation Node Module.

This module provides the ObservationNode class, which is responsible for
capturing and processing the outcomes of actions or tool executions.
"""

from __future__ import annotations

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class ObservationNode(BaseNode):
    """Node responsible for capturing observations from tool results.

    The ObservationNode processes the outputs of previously executed actions,
    effectively providing the "Observation" part of the ReAct cycle.
    """

    async def execute(self, state: AgentState) -> AgentState:
        """Captures an observation and updates the state history.

        Args:
            state: The current AgentState.

        Returns:
            The updated AgentState containing the observation message.
        """
        # Stub logic: execute tool 'check_status'
        if "messages" not in state:
            state["messages"] = []
        state["messages"].append({"role": "tool", "content": "Status: OK"})
        return state
