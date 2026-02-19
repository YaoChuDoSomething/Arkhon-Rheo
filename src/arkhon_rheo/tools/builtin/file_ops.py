"""File Operations Tool Module.

This module provides the FileOpsTool class, which enables agents to perform
basic reading and writing operations on the local filesystem.
"""

from __future__ import annotations

from pathlib import Path
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
    description = "Read or write files. Input format: 'read:path' or 'write:path:content'"

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
            self.allowed_directories = [Path.cwd()]
        else:
            self.allowed_directories = [Path(d).resolve() for d in allowed_directories]

    def _validate_path(self, file_path: str) -> Path:
        """Validate that the file path is within an allowed directory.

        Args:
            file_path: The path to validate.

        Returns:
            The Path object if valid.

        Raises:
            PermissionError: If the path is not allowed.
        """
        target_path = Path(file_path).resolve()

        # Check if path is within any allowed directory
        is_allowed = any(
            target_path == allowed_dir or allowed_dir in target_path.parents for allowed_dir in self.allowed_directories
        )

        if not is_allowed:
            raise PermissionError(
                f"Access to '{file_path}' is denied. Path is not within allowed directories: {self.allowed_directories}"
            )

        return target_path

    MAX_SPLITS = 2

    def run(self, **kwargs: Any) -> str:
        """Perform a file read or write operation.

        Args:
            **kwargs: Keyword arguments containing 'tool_input'.

        Returns:
            The file content for a 'read' operation, or a success/error message.
        """
        tool_input = kwargs.get("tool_input")
        if not isinstance(tool_input, str):
            return "Error: Invalid input. Expected 'tool_input' as a string."

        parts = tool_input.split(":", self.MAX_SPLITS)

        if len(parts) < self.MAX_SPLITS:
            return "Error: Invalid input format. Expected 'operation:path'"

        operation = parts[0].strip()
        raw_path = parts[1].strip()
        content = parts[2] if len(parts) > self.MAX_SPLITS else None

        try:
            file_path = self._validate_path(raw_path)
            if operation == "read":
                return self._read_file(file_path)
            if operation == "write":
                return self._write_file(file_path, content)
            return f"Error: Unknown operation '{operation}'. Supported: 'read', 'write'."
        except (PermissionError, Exception) as e:
            return f"Error: {e}"

    def _read_file(self, file_path: Path) -> str:
        """Handle file reading."""
        if not file_path.exists():
            return f"Error: File '{file_path}' not found."
        try:
            return file_path.read_text()
        except Exception as e:
            return f"Error reading file: {e}"

    def _write_file(self, file_path: Path, content: str | None) -> str:
        """Handle file writing."""
        if content is None:
            return "Error: Content is required for write operation."
        try:
            file_path.write_text(content)
            return f"Successfully wrote to '{file_path}'."
        except Exception as e:
            return f"Error writing file: {e}"
