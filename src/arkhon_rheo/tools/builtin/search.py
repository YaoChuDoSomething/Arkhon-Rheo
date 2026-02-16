from pydantic import BaseModel, Field
from arkhon_rheo.tools.base import BaseTool


class SearchInput(BaseModel):
    query: str = Field(description="The search query string")


class SearchTool(BaseTool):
    name = "search"
    description = "Search the web for information."
    args_schema = SearchInput

    def run(self, query: str) -> str:  # type: ignore[override]
        # Stub implementation
        return f"Simulated search results for: {query}"
