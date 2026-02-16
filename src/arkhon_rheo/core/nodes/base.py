from abc import ABC, abstractmethod
from typing import Any, Callable
from arkhon_rheo.core.state import AgentState


class BaseNode(ABC):
    """
    Abstract base class for all nodes in the agentic graph.
    Implements the Callable interface for async execution.
    """

    async def __call__(self, state: AgentState) -> AgentState:
        """Entry point for the node execution."""
        return await self.execute(state)

    @abstractmethod
    async def execute(self, state: AgentState) -> AgentState:
        """
        Core logic of the node.
        Must be implemented by concrete classes.
        """
        pass
