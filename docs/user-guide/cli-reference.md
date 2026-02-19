# CLI Reference

The `arkhon-rheo` command-line tool is designed to accelerate your multi-agent development workflow.

## Commands

### `version`

Displays the current version of the Arkhon-Rheo framework.

```bash
arkhon-rheo --version
```

### `init`

Initializes a new Arkhon-Rheo project structure in the specified directory.

```bash
arkhon-rheo init <project_name>
```

**Arguments:**

- `target`: The name of the new project directory.

### `run`

*Status: Placeholder/Experimental*
Executes an Arkhon-Rheo workflow based on a configuration file.

```bash
arkhon-rheo run --config workflow.yaml
```

**Options:**

- `--config <path>`: Path to the workflow configuration file (default: `workflow.yaml`).

### `migrate`

Assists in migrating existing LangGraph components (subgraphs or specialized agents) to the Arkhon-Rheo framework.

```bash
arkhon-rheo migrate <target_path> --type <subgraph|agent>
```

**Arguments:**

- `target`: The path to the file or directory to migrate.

**Options:**

- `--type [subgraph|agent]`: The type of component being migrated (default: `subgraph`).
