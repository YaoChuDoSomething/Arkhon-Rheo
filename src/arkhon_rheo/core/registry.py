"""Agent Registry Module.

This module provides a singleton registry for agent discovery within the
Arkhon-Rheo framework. It allows agents to register themselves and others
to locate them by name.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arkhon_rheo.core.agent import Agent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Singleton registry for agent discovery.

    This class maintains a mapping of agent names to their instances,
    enabling agents to look each other up for communication.
    """

    _instance: AgentRegistry | None = None
    _agents: dict[str, Agent] = {}

    def __new__(cls) -> AgentRegistry:
        """Ensure singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            # Ensure _agents is initialized on the class only once
            if not hasattr(cls, "_agents") or cls._agents is None:
                cls._agents = {}
        return cls._instance

    @classmethod
    def register(cls, agent: Agent) -> None:
        """Register an agent instance.

        Args:
            agent: The agent instance to be registered.
        """
        if agent.name in cls._agents:
            logger.warning(f"Agent '{agent.name}' already registered (overwriting).")
        cls._agents[agent.name] = agent
        logger.debug(f"Registered agent: {agent.name}")

    @classmethod
    def get(cls, name: str) -> Agent | None:
        """Retrieve an agent by its unique name.

        Args:
            name: The name of the agent to look up.

        Returns:
            The agent instance if found, otherwise None.
        """
        return cls._agents.get(name)

    @classmethod
    def list_agents(cls) -> dict[str, Agent]:
        """List all currently registered agents.

        Returns:
            A dictionary mapping agent names to their instances.
        """
        return cls._agents.copy()

    @classmethod
    def clear(cls) -> None:
        """Clear the registry.

        This is primarily intended for use during unit testing to ensure
        a clean state.
        """
        cls._agents.clear()
