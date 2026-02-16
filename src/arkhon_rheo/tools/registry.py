from typing import Dict, List, Optional
from arkhon_rheo.tools.base import BaseTool


class ToolRegistry:
    """
    Registry for managing available tools.
    Singleton pattern usage is recommended but not enforced at class level to allow testing.
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool instance."""
        if tool.name in self._tools:
            # warn or overwrite? overwrite for flexibility
            pass
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Retrieve a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[BaseTool]:
        """List all registered tools."""
        return list(self._tools.values())

    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()


# Global singleton instance
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    return _registry
