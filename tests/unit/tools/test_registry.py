from typing import Any

from arkhon_rheo.tools.base import BaseTool
from arkhon_rheo.tools.registry import ToolRegistry


def test_tool_registry_registration():
    """Verify tools can be registered and retrieved."""

    registry = ToolRegistry()
    registry.clear()

    class MockTool(BaseTool):
        name = "mock_tool"
        description = "A mock tool"

        def run(self, **kwargs: Any) -> str:
            tool_input = kwargs.get("input", "")
            return f"Mock: {tool_input}"

    tool = MockTool()
    registry.register(tool)

    # Retrieve by name
    retrieved = registry.get_tool("mock_tool")
    assert retrieved is not None
    assert retrieved.name == "mock_tool"


def test_tool_registry_duplicate_registration_overwrite():
    """Verify duplicate registration overwrites existing tool."""
    registry = ToolRegistry()
    registry.clear()

    class MockTool(BaseTool):
        name = "mock_tool"
        description = "A mock tool"

        def run(self, **kwargs: Any) -> str:
            return ""

    t1 = MockTool()
    t2 = MockTool()

    registry.register(t1)
    # Should not raise
    registry.register(t2)

    assert registry.get_tool("mock_tool") == t2


def test_tool_registry_get_nonexistent():
    """Verify getting non-existent tool returns None or raises error."""
    registry = ToolRegistry()
    assert registry.get_tool("non_existent") is None
