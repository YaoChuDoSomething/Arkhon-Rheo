import os
from pathlib import Path

import pytest

from arkhon_rheo.tools.builtin.file_ops import FileOpsTool


class TestFileOpsSecurity:
    @pytest.fixture
    def tool(self, tmp_path):
        # Initialize tool with tmp_path as the only allowed directory
        return FileOpsTool(allowed_directories=[str(tmp_path)])

    def test_allowed_directory_access(self, tool, tmp_path):
        """Test accessing a file within the allowed directory."""
        file_path = tmp_path / "test.txt"
        # Input format: write:path:content
        tool.run(tool_input=f"write:{file_path}:hello")
        assert file_path.exists()
        # Input format: read:path
        result = tool.run(tool_input=f"read:{file_path}")
        assert "hello" in result

    def test_path_traversal_blocked(self, tool, tmp_path):
        """Test that accessing a file outside the allowed directory is blocked."""
        # Create a file outside the allowed directory (referenced via traversal)

        # Try to access it using .. traversal
        traversal_path = str(tmp_path / ".." / "external.txt")

        # Should return an error message
        result = tool.run(tool_input=f"read:{traversal_path}")
        assert "Error" in result
        assert "Access to" in result and "is denied" in result

    def test_absolute_path_blocked(self, tool, tmp_path):
        """Test that accessing an absolute path outside allowed dirs is blocked."""
        # Try to access a system file (safe check)
        # We use a dummy path that clearly isn't in tmp_path
        forbidden_path = str(Path("/etc/passwd").resolve())
        if os.name == "nt":
            forbidden_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"

        result = tool.run(tool_input=f"read:{forbidden_path}")
        assert "Error" in result
        assert "Access to" in result and "is denied" in result

    def test_default_cwd_restriction(self):
        """Test that default initialization restricts to CWD."""
        tool = FileOpsTool()
        cwd = Path.cwd()

        # Should deny parent of CWD
        denied_file = str(cwd.parent / "test_deny.txt")

        # We don't actually write, just check the validation logic
        result = tool.run(tool_input=f"read:{denied_file}")
        assert "Error" in result
        assert "Access to" in result and "is denied" in result
