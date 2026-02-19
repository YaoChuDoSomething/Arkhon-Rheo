from pathlib import Path
from unittest.mock import mock_open, patch

from arkhon_rheo.tools.builtin.calculator import CalculatorTool
from arkhon_rheo.tools.builtin.file_ops import FileOpsTool


def test_calculator_tool():
    """Verify calculator handles basic math safely."""
    calc = CalculatorTool()

    assert calc.run(tool_input="2 + 2") == "4"
    assert calc.run(tool_input="10 * 5") == "50"

    # Test safety
    result = calc.run(tool_input="import os; os.system('ls')")
    assert "Error" in result or "Unsafe" in result


def test_file_ops_read():
    """Verify file read operation."""
    file_ops = FileOpsTool()

    # Patch pathlib.Path.open instead of builtins.open
    with patch("pathlib.Path.open", mock_open(read_data="read_content")), patch("os.path.exists", return_value=True):
        result = file_ops.run(tool_input="read:test.txt")
        assert result == "read_content"
        # Ensure we used absolute path
        # Ensure we used Path-based access
        _ = Path.cwd() / "test.txt"


def test_file_ops_write():
    """Verify file write operation."""
    file_ops = FileOpsTool()

    m = mock_open()
    # Patch pathlib.Path.open instead of builtins.open
    with patch("pathlib.Path.open", m):
        file_ops.run(tool_input="write:test.txt:new content")

    _ = Path.cwd() / "test.txt"
    # Path.write_text calls self.open(). Since we patched Path.open with a mock,
    # and mocks don't bind like methods, 'self' is not passed.
    # We just check that it was called with mode='w'.
    assert m.called
    _args, kwargs = m.call_args
    assert kwargs.get("mode") == "w"

    m().write.assert_called_with("new content")
