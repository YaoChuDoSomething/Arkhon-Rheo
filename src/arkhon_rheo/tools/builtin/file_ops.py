"""File Operations Tool Module.

This module provides the FileOpsTool class, which enables agents to perform
basic reading and writing operations on the local filesystem.
"""

from __future__ import annotations

import os
from typing import Any

from arkhon_rheo.tools.base import BaseTool


class FileOpsTool(BaseTool):
    """Tool for performing basic file operations.

    Supports reading and writing text files using a colon-separated input
    format.

    Attributes:
        allowed_directories: List of absolute paths that the tool is permitted to access.
    """

    name = "file_ops"
    description = (
        "Read or write files. Input format: 'read:path' or 'write:path:content'"
    )

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        allowed_directories: list[str] | None = None,
    ):
        """Initialize the FileOpsTool.

        Args:
            name: Optional override for tool name.
            description: Optional override for tool description.
            allowed_directories: List of directories allowed for file access.
                               Defaults to current working directory.
        """
        super().__init__(name, description)
        if allowed_directories is None:
            self.allowed_directories = [os.getcwd()]
        else:
            self.allowed_directories = [os.path.abspath(d) for d in allowed_directories]

    def _validate_path(self, file_path: str) -> str:
        """Validate that the file path is within an allowed directory.

        Args:
            file_path: The path to validate.

        Returns:
            The absolute path if valid.

        Raises:
            PermissionError: If the path is not allowed.
        """
        abs_path = os.path.abspath(file_path)

        # Check if path is within any allowed directory
        is_allowed = False
        for allowed_dir in self.allowed_directories:
            try:
                # Use commonpath to check if allowed_dir is a prefix of abs_path
                # This handles ../ traversal correctly because paths are abspath'd
                if os.path.commonpath([allowed_dir, abs_path]) == allowed_dir:
                    is_allowed = True
                    break
            except ValueError:
                # commonpath raises ValueError if paths are on different drives (Windows)
                continue

        if not is_allowed:
            raise PermissionError(
                f"Access to '{file_path}' is denied. Path is not within allowed directories: {self.allowed_directories}"
            )

        return abs_path

    def run(self, input: str, **kwargs: Any) -> str:
        """Perform a file read or write operation.

        Args:
            input: A string in the format 'operation:path[:content]'.
            **kwargs: Additional keyword arguments (ignored).

        Returns:
            The file content for a 'read' operation, or a success/error message.
        """
        parts = input.split(":", 2)

        if len(parts) < 2:
            return "Error: Invalid input format. Expected 'operation:path'"

        operation = parts[0].strip()
        raw_path = parts[1].strip()
        content = parts[2] if len(parts) > 2 else None

        try:
            file_path = self._validate_path(raw_path)
        except PermissionError as e:
            return f"Error: {str(e)}"

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
