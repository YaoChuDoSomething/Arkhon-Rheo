from pathlib import Path

from click.testing import CliRunner

from arkhon_rheo.cli.main import init


def test_init_directory_traversal_prevention(tmp_path):
    """Test that init command prevents directory traversal in project name."""
    runner = CliRunner()

    # Run in a temporary directory
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Attempt traversal using ..
        result = runner.invoke(init, ["../malicious_project"])

        # Should fail with an error message
        assert result.exit_code != 0
        assert "Error" in result.output or "Invalid project name" in result.output

        # Verify directory was not created outside
        assert not (tmp_path.parent / "malicious_project").exists()


def test_init_invalid_characters(tmp_path):
    """Test that init command prevents invalid characters in project name."""
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Attempt using path separator
        result = runner.invoke(init, ["sub/dir/project"])

        assert result.exit_code != 0
        assert "Error" in result.output or "Invalid project name" in result.output


def test_init_valid_name(tmp_path):
    """Test that init command accepts valid project names."""
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(init, ["valid_project"])

        assert result.exit_code == 0
        assert Path("valid_project").exists()
        assert (Path("valid_project") / "pyproject.toml").exists()
