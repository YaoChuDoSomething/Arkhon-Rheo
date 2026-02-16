import pytest
from arkhon_rheo.core.tools.base import BaseTool
from arkhon_rheo.core.tools.registry import ToolRegistry


def test_tool_registry_registration():
    """Verify tools can be registered and retrieved."""

    registry = ToolRegistry()

    class MockTool(BaseTool):
        name = "mock_tool"
        description = "A mock tool"

        def run(self, input: str) -> str:
            return f"Mock: {input}"

    tool = MockTool()
    registry.register(tool)

    # Retrieve by name
    retrieved = registry.get("mock_tool")
    assert retrieved == tool
    assert retrieved.name == "mock_tool"


def test_tool_registry_duplicate_registration():
    """Verify duplicate registration raises error."""
    registry = ToolRegistry()

    class MockTool(BaseTool):
        name = "mock_tool"
        description = "A mock tool"

        def run(self, input: str) -> str:
            return ""

    t1 = MockTool()
    t2 = MockTool()

    registry.register(t1)
    with pytest.raises(ValueError):
        registry.register(t2)


def test_tool_registry_get_nonexistent():
    """Verify getting non-existent tool returns None or raises error."""
    registry = ToolRegistry()
    assert registry.get("non_existent") is None
