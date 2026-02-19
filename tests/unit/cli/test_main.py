from pathlib import Path

from click.testing import CliRunner

from arkhon_rheo.cli.main import main


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
        p = Path(project_name)
        assert p.exists()
        assert (p / "agents").is_dir()
        assert (p / "tools").is_dir()
        assert (p / "pyproject.toml").exists()


def test_cli_run_help():
    """Test that arkhon-rheo run --help shows usage instructions."""
    runner = CliRunner()
    result = runner.invoke(main, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run an Arkhon-Rheo workflow" in result.output


def test_cli_migrate_success():
    """Test that arkhon-rheo migrate command works with target."""
    runner = CliRunner()
    result = runner.invoke(main, ["migrate", "my_subgraph", "--type", "subgraph"])
    assert result.exit_code == 0
    assert "Analyzing subgraph at: my_subgraph" in result.output
    assert "Migration analysis complete" in result.output
