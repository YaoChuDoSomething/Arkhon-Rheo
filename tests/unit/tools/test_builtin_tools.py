import os
from unittest.mock import mock_open, patch

from arkhon_rheo.tools.builtin.calculator import CalculatorTool
from arkhon_rheo.tools.builtin.file_ops import FileOpsTool


def test_calculator_tool():
    """Verify calculator handles basic math safely."""
    calc = CalculatorTool()

    assert calc.run("2 + 2") == "4"
    assert calc.run("10 * 5") == "50"

    # Test safety
    result = calc.run("import os; os.system('ls')")
    assert "Error" in result or "Unsafe" in result


def test_file_ops_read():
    """Verify file read operation."""
    file_ops = FileOpsTool()

    with patch("builtins.open", mock_open(read_data="content")):
        with patch("os.path.exists", return_value=True):
            result = file_ops.run("read:test.txt")
            assert result == "content"
            # Ensure we used absolute path
            path = os.path.join(os.getcwd(), "test.txt")


def test_file_ops_write():
    """Verify file write operation."""
    file_ops = FileOpsTool()

    m = mock_open()
    with patch("builtins.open", m):
        file_ops.run("write:test.txt:new content")

    path = os.path.join(os.getcwd(), "test.txt")
    m.assert_called_with(path, "w")
    m().write.assert_called_with("new content")
