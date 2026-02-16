from abc import ABC, abstractmethod
from typing import Optional
from arkhon_rheo.core.state import ReActState


class BaseRule(ABC):
    """
    Abstract base class for validation rules.
    """

    name: str

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def check(self, state: ReActState) -> Optional[str]:
        """
        Check the state against the rule.
        Returns:
            Optional[str]: Error message if rule is violated, None otherwise.
        """
        pass
