"""RACI Workflow Configuration Loader.

Loads and validates `config/workflow_context.yaml` into a `RACIWorkflowConfig`
Pydantic model. This is separate from the base `ConfigLoader` to keep the
RACI concern isolated.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from arkhon_rheo.config.schema import RACIWorkflowConfig

_DEFAULT_CONFIG_PATH = Path(__file__).parents[4] / "config" / "workflow_context.yaml"


def load_raci_config(config_path: str | Path | None = None) -> RACIWorkflowConfig:
    """Load and validate the RACI workflow configuration.

    Args:
        config_path: Path to the YAML file.  Defaults to
            ``<project_root>/config/workflow_context.yaml``.

    Returns:
        A validated :class:`RACIWorkflowConfig` instance.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If the YAML is malformed or Pydantic validation fails.
    """
    path = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH

    if not path.exists():
        raise FileNotFoundError(f"RACI config not found: {path}")

    try:
        raw: dict = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML parse error in {path}: {exc}") from exc

    try:
        return RACIWorkflowConfig(**raw)
    except ValidationError as exc:
        raise ValueError(f"RACI config validation failed: {exc}") from exc
