"""Tool Registry Module.

This module provides the ToolRegistry class and a global singleton instance
for managing and discovering available tools within the Arkhon-Rheo framework.
"""

from __future__ import annotations

from arkhon_rheo.tools.base import BaseTool


class ToolRegistry:
    """Registry for managing and discovering available tools.

    Provides a centralized location for registering tool instances and
    retrieving them by name for execution by agents.
    """

    def __init__(self) -> None:
        """Initialize a ToolRegistry instance."""
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool instance in the registry.

        If a tool with the same name already exists, it will be overwritten.

        Args:
            tool: An instance of a class inheriting from BaseTool.
        """
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool | None:
        """Retrieve a registered tool by its name.

        Args:
            name: The name of the tool to retrieve.

        Returns:
            The BaseTool instance if found, otherwise None.
        """
        return self._tools.get(name)

    def list_tools(self) -> list[BaseTool]:
        """List all currently registered tool instances.

        Returns:
            A list of all BaseTool instances in the registry.
        """
        return list(self._tools.values())

    def clear(self) -> None:
        """Clear all tool registrations from the registry.

        This is primarily useful for resetting the state between tests.
        """
        self._tools.clear()


# Global singleton instance
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """Retrieve the global singleton ToolRegistry instance.

    Returns:
        The global ToolRegistry instance.
    """
    return _registry
