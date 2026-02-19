"""Configuration Loader Module.

This module provides the ConfigLoader class, which handles the acquisition,
parsing, and validation of framework configurations from various sources
like YAML files and environment variables.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from arkhon_rheo.config.schema import ArkhonConfig


class ConfigLoader:
    """Loads and validates configuration data.

    Coordinates the loading of raw data from the filesystem and maps it to
    the structured ArkhonConfig Pydantic model, ensuring all required
    parameters are present and correctly typed.

    Attributes:
        config_path: The filesystem path to the YAML configuration file.
    """

    def __init__(self, config_path: str | None = None) -> None:
        """Initialize a ConfigLoader instance.

        Args:
            config_path: Optional path to a YAML configuration file.
        """
        self.config_path = config_path

    def load(self) -> ArkhonConfig:
        """Load and validate the configuration.

        Returns:
            An instance of ArkhonConfig populated with the loaded data.

        Raises:
            ValueError: If the YAML is malformed or validation fails.
            FileNotFoundError: If the specified config file does not exist.
        """
        config_data: dict[str, Any] = {}

        # Load from file if exists
        if self.config_path:
            path = Path(self.config_path)
            if path.exists():
                try:
                    with path.open() as f:
                        config_data = yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    raise ValueError(f"Error parsing YAML file: {e}") from e
            else:
                raise FileNotFoundError(f"Config file not found: {self.config_path}")

        # Validate with Pydantic
        try:
            return ArkhonConfig(**config_data)
        except ValidationError as e:
            raise ValueError(f"Configuration validation failed: {e}") from e

    @staticmethod
    def load_from_env() -> ArkhonConfig:
        """Stub for loading configuration from environment variables.

        Currently returns a default ArkhonConfig instance.

        Returns:
            An ArkhonConfig instance.
        """
        # In real implementation, we would map ARKHON_LLM_MODEL -> llm.model etc.
        return ArkhonConfig()
