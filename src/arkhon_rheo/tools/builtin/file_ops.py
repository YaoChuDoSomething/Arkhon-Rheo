import os
from arkhon_rheo.core.tools.base import BaseTool


class FileOpsTool(BaseTool):
    name = "file_ops"
    description = (
        "Read or write files. Input format: 'read:path' or 'write:path:content'"
    )

    def run(self, input: str) -> str:
        parts = input.split(":", 2)
        operation = parts[0].strip()

        if len(parts) < 2:
            return "Error: Invalid input format. Expected 'operation:path'"

        file_path = parts[1].strip()
        content = parts[2] if len(parts) > 2 else None

        if operation == "read":
            try:
                if not os.path.exists(file_path):
                    return f"Error: File '{file_path}' not found."
                with open(file_path, "r") as f:
                    return f.read()
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
