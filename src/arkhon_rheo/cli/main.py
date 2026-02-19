"""Main CLI Entry Point.

This module defines the command-line interface for the Arkhon-Rheo framework,
providing tools for project initialization, workflow execution, and
component migration.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path

import click

from arkhon_rheo.cli.migrate import migrate_agent, migrate_subgraph
from arkhon_rheo.config.raci_loader import load_raci_config
from arkhon_rheo.orchestrator.meta_graph import meta_orchestrator_graph
from arkhon_rheo.workflows.base import build_state


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
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        click.echo(f"Error: Invalid project name '{name}'. Only letters, digits, hyphens, and underscores are allowed.")
        sys.exit(1)

    target_path = Path(name)

    click.echo(f"🚀 Initializing Arkhon-Rheo project: {name}...")
    (target_path / "agents").mkdir(parents=True, exist_ok=True)
    (target_path / "tools").mkdir(parents=True, exist_ok=True)

    with (target_path / "pyproject.toml").open("w") as f:
        f.write(f'[project]\nname = "{name}"\nversion = "0.1.0"\n')
    click.echo("✨ Done.")


@main.command()
@click.option("--config", default="workflow.yaml", help="Path to workflow configuration.")
def run(config: str) -> None:
    """Run an Arkhon-Rheo workflow using a configuration file.

    Args:
        config: Path to the YAML file defining the workflow.
    """
    click.echo(f"🚀 Running Arkhon-Rheo workflow with config: {config}")

    try:
        load_raci_config(config)
        prompt = click.prompt("Enter task description")

        state = build_state(prompt)

        # Execute Meta-Orchestrator
        click.echo("🧠 Evaluating task complexity and selecting RACI scheme...")
        result = asyncio.run(meta_orchestrator_graph.ainvoke(state))

        click.echo("✅ Workflow completed.")
        selected = result["shared_context"].get("selected_scheme")
        click.echo(f"🎯 Selected Scheme: {selected}")
        click.echo(f"📝 Reasoning: {result['shared_context'].get('evaluation_reasoning')}")

    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@main.command()
@click.argument("target")
@click.option("--type", "target_type", type=click.Choice(["subgraph", "agent"]), default="subgraph")
def migrate(target: str, target_type: str) -> None:
    """Migrate LangGraph components to Arkhon-Rheo.

    Translates existing LangGraph node/edge logic into Arkhon-Rheo compatibles.

    Args:
        target: The file or directory to migrate.
        type: The type of component being migrated ('subgraph' or 'agent').
    """
    if target_type == "subgraph":
        migrate_subgraph(target)
    else:
        migrate_agent(target)


if __name__ == "__main__":
    main()
