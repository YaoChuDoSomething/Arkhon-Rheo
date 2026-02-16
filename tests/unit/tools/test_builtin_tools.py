from arkhon_rheo.tools.builtin.search import SearchTool
from arkhon_rheo.tools.builtin.calculator import CalculatorTool
from arkhon_rheo.tools.builtin.file_ops import FileOpsTool


def test_search_tool():
    tool = SearchTool()
    result = tool.run(query="test query")
    assert "Simulated search results" in result
    assert "test query" in result


def test_calculator_tool():
    tool = CalculatorTool()
    assert tool.run(expression="1 + 1") == "2"
    assert tool.run(expression="math.sqrt(4)") == "2.0"
    # Test error handling
    assert "Error" in tool.run(expression="1 / 0")


def test_file_ops_tool(tmp_path):
    tool = FileOpsTool()
    file_path = tmp_path / "test.txt"

    # Write
    result = tool.run(operation="write", file_path=str(file_path), content="Hello")
    assert "Successfully wrote" in result
    assert file_path.read_text() == "Hello"

    # Read
    content = tool.run(operation="read", file_path=str(file_path))
    assert content == "Hello"

    # Error cases
    assert "Error" in tool.run(
        operation="read", file_path=str(tmp_path / "missing.txt")
    )
    assert "Error" in tool.run(operation="unknown", file_path=str(file_path))
