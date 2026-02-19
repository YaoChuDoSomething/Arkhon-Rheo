"""Commit Node Module.

This module provides the CommitNode class, which is responsible for
finalizing and persisting the results of a workflow or graph execution.
"""

from __future__ import annotations

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class CommitNode(BaseNode):
    """Node responsible for committing results or state checkpoints.

    The CommitNode marks a successful conclusion of a logical unit of work,
    ensuring that the final state is correctly flagged for persistence or
    downstream consumption.
    """

    async def execute(self, state: AgentState) -> AgentState:
        """Finalize the current state by marking it as committed.

        Args:
            state: The current AgentState.

        Returns:
            The AgentState with the committed flag set in shared context.
        """
        if "shared_context" not in state:
            state["shared_context"] = {}
        state["shared_context"]["committed"] = True
        return state
