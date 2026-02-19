"""Governance Nodes Module.

This module provides nodes specialized for governance and oversight within
the Arkhon-Rheo framework, including decision-making based on RACI roles
and status broadcasting to informed parties.
"""

from __future__ import annotations

import logging

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode

logger = logging.getLogger(__name__)


class GovernanceNode(BaseNode):
    """Base class for governance-related nodes."""

    pass


class DecisionNode(GovernanceNode):
    """Node that evaluates results and routes based on a verdict.

    Evaluates the current state (specifically shared context or agent responses)
    to determine the next step in the graph, simulating an Accountable
    agent's oversight.

    Attributes:
        accountable_agent_name: the name of the agent responsible for the verdict.
    """

    def __init__(self, accountable_agent_name: str) -> None:
        """Initialize a DecisionNode instance.

        Args:
            accountable_agent_name: Name of the agent providing the verdict.
        """
        super().__init__()
        self.accountable_agent_name = accountable_agent_name

    async def execute(self, state: AgentState) -> AgentState:
        """Evaluate the verdict and set the next execution step.

        Args:
            state: The current AgentState.

        Returns:
            The AgentState with an updated 'next_step'.
        """
        messages = state.get("messages", [])
        if not messages:
            return state

        # In a real implementation, we would invoke the Accountable agent here
        # or check a specific field in the state where the verdict was placed.
        verdict = state.get("shared_context", {}).get("verdict")

        if verdict == "approved":
            state["next_step"] = "END"
        elif verdict == "rejected":
            # Repurpose current_task to find where to go back
            state["next_step"] = state.get("current_task", "START")

        logger.info(
            f"DecisionNode: Accountable agent '{self.accountable_agent_name}' verdict: {verdict}"
        )
        return state


class InformNode(GovernanceNode):
    """Node that broadcasts status updates to 'Informed' agents.

    Following the RACI model, this node identifies agents that need to be
    notified about a task's progress and logs/sends notifications to them.
    """

    async def execute(self, state: AgentState) -> AgentState:
        """Notify informed agents about the current task status.

        Args:
            state: The current AgentState (expected to have RACI context).

        Returns:
            The AgentState (unchanged).
        """
        current_task = state.get("current_task")
        if not current_task:
            return state

        raci = state.get("raci_config", {}).get(current_task)
        if not raci:
            return state

        informed_agents = raci.get("informed", [])
        last_msg = state["messages"][-1] if state.get("messages") else "No content"

        for agent_name in informed_agents:
            logger.info(
                f"NOTIFICATION to {agent_name}: Task '{current_task}' status updated. Result: {last_msg}"
            )

        return state
