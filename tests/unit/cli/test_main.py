import pytest
from click.testing import CliRunner
from arkhon_rheo.cli.main import main
import os


def test_cli_version():
    """Test that arkhon-rheo --version returns the correct version."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "arkhon-rheo, version 0.1.0" in result.output


def test_cli_init_success(tmp_path):
    """Test that arkhon-rheo init creates the project structure."""
    runner = CliRunner()
    project_name = "test_project"
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ["init", project_name])
        assert result.exit_code == 0
        assert f"Initializing Arkhon-Rheo project: {project_name}" in result.output
        assert "Done" in result.output
        assert os.path.exists(project_name)
        assert os.path.isdir(os.path.join(project_name, "agents"))
        assert os.path.isdir(os.path.join(project_name, "tools"))
        assert os.path.exists(os.path.join(project_name, "pyproject.toml"))


def test_cli_run_help():
    """Test that arkhon-rheo run --help shows usage instructions."""
    runner = CliRunner()
    result = runner.invoke(main, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run an Arkhon-Rheo workflow" in result.output


def test_cli_migrate_placeholder():
    """Test that arkhon-rheo migrate command exists as a placeholder."""
    runner = CliRunner()
    result = runner.invoke(main, ["migrate", "--help"])
    assert result.exit_code == 0
    assert "Migrate LangGraph components to Arkhon-Rheo" in result.output
