"""Base Node Module.

This module defines the BaseNode abstract class, which serves as the foundation
for all execution nodes within the Arkhon-Rheo framework, providing
standardized lifecycle hooks and error handling.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from arkhon_rheo.core.context import ContextManager
from arkhon_rheo.core.state import AgentState

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """Abstract base class for all execution nodes.

    Implements a structured execution lifecycle (before_execute -> execute ->
    after_execute) to ensure consistent behavior, logging, and state
    management across different node types.

    Attributes:
        context: The execution context manager for this node.
    """

    def __init__(self, context: ContextManager | None = None) -> None:
        """Initialize a BaseNode instance.

        Args:
            context: Optional context manager for managing thread-local state.
        """
        self.context = context or ContextManager()

    async def __call__(self, state: AgentState) -> AgentState:
        """EntryPoint for the node execution.

        Wraps the core execution logic in lifecycle hooks and handles
        unexpected exceptions.

        Args:
            state: The current AgentState before execution.

        Returns:
            The modified AgentState after execution.

        Raises:
            Exception: Re-raises any exceptions encountered during execution for
                upstream handling.
        """
        try:
            self.before_execute(state)
            new_state = await self.execute(state)
            self.after_execute(new_state)
            return new_state
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}", exc_info=True)
            raise e

    def before_execute(self, state: AgentState) -> None:
        """Hook executed immediately before the core logic.

        Args:
            state: The incoming AgentState.
        """
        logger.debug(f"Entering {self.__class__.__name__}")

    @abstractmethod
    async def execute(self, state: AgentState) -> AgentState:
        """The core logic of the node.

        Must be implemented by concrete subclasses.

        Args:
            state: The incoming AgentState.

        Returns:
            the modified AgentState.
        """
        pass

    def after_execute(self, state: AgentState) -> None:
        """Hook executed immediately after the core logic successfully finishes.

        Args:
            state: The outgoing AgentState.
        """
        logger.debug(f"Exiting {self.__class__.__name__}")
