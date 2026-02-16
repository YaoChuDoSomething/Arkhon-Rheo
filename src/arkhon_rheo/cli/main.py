import click
import os
from arkhon_rheo import __version__
from arkhon_rheo.cli.migrate import migrate_subgraph, migrate_agent


@click.group()
@click.version_option(version="0.1.0", prog_name="arkhon-rheo")
def main():
    """Arkhon-Rheo CLI - Unified Multi-Agent Framework"""
    pass


@main.command()
@click.argument("name")
def init(name):
    """Initialize a new Arkhon-Rheo project structure."""
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
def run(config):
    """Run an Arkhon-Rheo workflow."""
    click.echo(f"Running workflow with config: {config}")
    # Implementation placeholder
    pass


@main.command()
@click.argument("target")
@click.option("--type", type=click.Choice(["subgraph", "agent"]), default="subgraph")
def migrate(target, type):
    """Migrate LangGraph components to Arkhon-Rheo."""
    if type == "subgraph":
        migrate_subgraph(target)
    else:
        migrate_agent(target)


if __name__ == "__main__":
    main()
