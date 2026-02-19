"""Main CLI Entry Point.

This module defines the command-line interface for the Arkhon-Rheo framework,
providing tools for project initialization, workflow execution, and
component migration.
"""

from __future__ import annotations

import os
import sys

import click

from arkhon_rheo.cli.migrate import migrate_agent, migrate_subgraph


@click.group()
@click.version_option(version="0.1.0", prog_name="arkhon-rheo")
def main() -> None:
    """Arkhon-Rheo CLI - Unified Multi-Agent Framework."""
    pass


@main.command()
@click.argument("name")
def init(name: str) -> None:
    """Initialize a new Arkhon-Rheo project structure.

    Creates the basic directory hierarchy and a boilerplate pyproject.toml
    for a new agent-based project.

    Args:
        name: The name of the new project to create.
    """
    if os.sep in name or ".." in name:
        click.echo(
            f"Error: Invalid project name '{name}'. cannot contain path separators or '..'."
        )
        sys.exit(1)

    click.echo(f"🚀 Initializing Arkhon-Rheo project: {name}...")
    os.makedirs(name, exist_ok=True)
    os.makedirs(os.path.join(name, "agents"), exist_ok=True)
    os.makedirs(os.path.join(name, "tools"), exist_ok=True)
    with open(os.path.join(name, "pyproject.toml"), "w") as f:
        f.write(f'[project]\nname = "{name}"\nversion = "0.1.0"\n')
    click.echo("✨ Done.")


@main.command()
@click.option(
    "--config", default="workflow.yaml", help="Path to workflow configuration."
)
def run(config: str) -> None:
    """Run an Arkhon-Rheo workflow using a configuration file.

    Args:
        config: Path to the YAML file defining the workflow.
    """
    click.echo(f"Running workflow with config: {config}")
    # Implementation placeholder
    pass


@main.command()
@click.argument("target")
@click.option("--type", type=click.Choice(["subgraph", "agent"]), default="subgraph")
def migrate(target: str, type: str) -> None:
    """Migrate LangGraph components to Arkhon-Rheo.

    Translates existing LangGraph node/edge logic into Arkhon-Rheo compatibles.

    Args:
        target: The file or directory to migrate.
        type: The type of component being migrated ('subgraph' or 'agent').
    """
    if type == "subgraph":
        migrate_subgraph(target)
    else:
        migrate_agent(target)


if __name__ == "__main__":
    main()
