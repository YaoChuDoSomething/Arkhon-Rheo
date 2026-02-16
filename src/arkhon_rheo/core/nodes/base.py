from abc import ABC, abstractmethod
from typing import Any, Callable
from arkhon_rheo.core.state import ReActState


class BaseNode(ABC):
    """
    Abstract base class for all nodes in the ReAct graph.
    Implements the Callable interface to allow nodes to be used as functions.
    """

    def __call__(self, state: ReActState) -> ReActState:
        """Entry point for the node execution."""
        return self.execute(state)

    @abstractmethod
    def execute(self, state: ReActState) -> ReActState:
        """
        Core logic of the node.
        Must be implemented by concrete classes.
        """
        pass
