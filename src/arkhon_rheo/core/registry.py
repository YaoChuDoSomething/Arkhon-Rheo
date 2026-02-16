from typing import Dict, Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from arkhon_rheo.core.agent import Agent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Singleton registry for agent discovery.
    """

    _instance = None
    _agents: Dict[str, "Agent"] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._agents = {}
        return cls._instance

    @classmethod
    def register(cls, agent: "Agent") -> None:
        """Register an agent instance."""
        if agent.name in cls._agents:
            logger.warning(f"Agent '{agent.name}' already registered (overwriting).")
        cls._agents[agent.name] = agent
        logger.debug(f"Registered agent: {agent.name}")

    @classmethod
    def get(cls, name: str) -> Optional["Agent"]:
        """Get an agent by name."""
        return cls._agents.get(name)

    @classmethod
    def list_agents(cls) -> Dict[str, "Agent"]:
        """List all registered agents."""
        return cls._agents.copy()

    @classmethod
    def clear(cls) -> None:
        """Clear the registry (useful for testing)."""
        cls._agents.clear()
