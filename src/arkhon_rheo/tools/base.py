"""Base Tool Module.

This module defines the abstract base class for all tools in the Arkhon-Rheo
framework, utilizing Pydantic for robust input schema definition and validation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseTool(ABC):
    """Abstract base class for all tools.

    Tools provide specific functionalities (e.g., calculations, file operations)
    that agents can invoke. They use Pydantic models to define and validate
    their input arguments.

    Attributes:
        name: The unique name of the tool.
        description: A concise description of what the tool does.
        args_schema: Optional Pydantic model for validating tool arguments.
    """

    name: str
    description: str
    args_schema: type[BaseModel] | None = None

    def __init__(self, name: str | None = None, description: str | None = None) -> None:
        """Initialize a BaseTool instance.

        Args:
            name: Override the default tool name.
            description: Override the default tool description.
        """
        self.name = name or self.name
        self.description = description or self.description

    @property
    def schema(self) -> dict[str, Any]:
        """Return the JSON schema for the tool arguments.

        Returns:
            A dictionary representing the JSON schema of args_schema.
        """
        if self.args_schema:
            return self.args_schema.model_json_schema()
        return {"type": "object", "properties": {}}

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """Execute the core tool logic.

        Must be implemented by subclasses.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to tool inputs.

        Returns:
            The result of the tool execution.
        """
        pass

    def __call__(self, **kwargs: Any) -> Any:
        """Invoke the tool by calling the instance.

        Args:
            **kwargs: Arguments to pass to the tool's run method.

        Returns:
            The tool's execution result.
        """
        # TODO: Add validation against args_schema here
        return self.run(**kwargs)
