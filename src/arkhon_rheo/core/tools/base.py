from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseTool(ABC):
    """
    Abstract base class for all tools.
    """

    name: str
    description: str

    @abstractmethod
    def run(self, input: Any) -> Any:
        """
        Execute the tool logic.
        """
        pass

    def __call__(self, input: Any) -> Any:
        return self.run(input)
