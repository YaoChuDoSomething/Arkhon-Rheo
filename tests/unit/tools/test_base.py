from pydantic import BaseModel, Field

from arkhon_rheo.tools.base import BaseTool
from arkhon_rheo.tools.registry import ToolRegistry


class SearchInput(BaseModel):
    query: str = Field(description="Search query")


class MockSearchTool(BaseTool):
    name = "search"
    description = "Searches the web"
    args_schema = SearchInput

    def run(self, query: str) -> str:  # type: ignore[override]
        return f"Results for: {query}"


def test_base_tool_schema():
    tool = MockSearchTool()
    schema = tool.schema
    assert "query" in schema["properties"]
    assert tool.name == "search"


def test_tool_registry():
    registry = ToolRegistry()
    tool = MockSearchTool()

    registry.register(tool)
    assert registry.get_tool("search") == tool
    assert len(registry.list_tools()) == 1

    registry.clear()
    assert len(registry.list_tools()) == 0
