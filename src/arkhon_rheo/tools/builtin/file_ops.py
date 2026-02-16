from typing import Optional
from pydantic import BaseModel, Field
from arkhon_rheo.tools.base import BaseTool


class FileOpsInput(BaseModel):
    operation: str = Field(description="Operation to perform: 'read' or 'write'")
    file_path: str = Field(description="Path to the file")
    content: Optional[str] = Field(
        default=None, description="Content to write (required for 'write')"
    )


class FileOpsTool(BaseTool):
    name = "file_ops"
    description = "Read or write files to the local filesystem."
    args_schema = FileOpsInput

    def run(self, operation: str, file_path: str, content: Optional[str] = None) -> str:  # type: ignore[override]
        # Security: In real production, we must sandbox this to a specific directory.
        # For this exercise, we assume it's running in a controlled env.

        if operation == "read":
            try:
                with open(file_path, "r") as f:
                    return f.read()
            except FileNotFoundError:
                return f"Error: File '{file_path}' not found."
            except Exception as e:
                return f"Error reading file: {str(e)}"

        elif operation == "write":
            if content is None:
                return "Error: Content is required for write operation."
            try:
                with open(file_path, "w") as f:
                    f.write(content)
                return f"Successfully wrote to '{file_path}'."
            except Exception as e:
                return f"Error writing file: {str(e)}"

        else:
            return (
                f"Error: Unknown operation '{operation}'. Supported: 'read', 'write'."
            )
