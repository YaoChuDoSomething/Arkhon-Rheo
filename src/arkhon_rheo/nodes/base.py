from abc import ABC, abstractmethod
from typing import Optional
import logging
from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.context import ContextManager

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """
    Abstract base class for all ReAct nodes.
    Implements lifecycle hooks: before_execute -> execute -> after_execute.
    """

    def __init__(self, context: Optional[ContextManager] = None):
        self.context = context or ContextManager()

    def __call__(self, state: ReActState) -> ReActState:
        """Entry point for the node execution."""
        try:
            self.before_execute(state)
            new_state = self.execute(state)
            self.after_execute(new_state)
            return new_state
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}", exc_info=True)
            # In a real system we might want to return an error state or re-raise
            # For now re-raise to fail fast during dev
            raise e

    def before_execute(self, state: ReActState) -> None:
        """Hook to run before execution logic."""
        logger.debug(f"Entering {self.__class__.__name__}")

    @abstractmethod
    def execute(self, state: ReActState) -> ReActState:
        """Core logic of the node. Must be implemented by subclasses."""
        pass

    def after_execute(self, state: ReActState) -> None:
        """Hook to run after execution logic."""
        logger.debug(f"Exiting {self.__class__.__name__}")
