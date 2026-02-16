from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Optional
from pydantic import BaseModel


class BaseTool(ABC):
    """
    Abstract base class for all tools.
    Uses Pydantic for input schema definition.
    """

    name: str
    description: str
    args_schema: Optional[Type[BaseModel]] = None

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name or self.name
        self.description = description or self.description

    @property
    def schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool arguments."""
        if self.args_schema:
            return self.args_schema.model_json_schema()
        return {"type": "object", "properties": {}}

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """Execute the tool logic."""
        pass

    def __call__(self, **kwargs: Any) -> Any:
        # TODO: Add validation against args_schema here
        return self.run(**kwargs)
