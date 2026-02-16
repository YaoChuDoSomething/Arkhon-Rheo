import yaml
from typing import Optional, Dict, Any
from pathlib import Path
from pydantic import ValidationError
from arkhon_rheo.config.schema import ArkhonConfig


class ConfigLoader:
    """
    Loads and validates configuration from YAML files and environment variables.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path

    def load(self) -> ArkhonConfig:
        """Load configuration."""
        config_data: Dict[str, Any] = {}

        # Load from file if exists
        if self.config_path:
            path = Path(self.config_path)
            if path.exists():
                try:
                    with open(path, "r") as f:
                        config_data = yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    raise ValueError(f"Error parsing YAML file: {e}")
            else:
                raise FileNotFoundError(f"Config file not found: {self.config_path}")

        # Validate with Pydantic
        try:
            config = ArkhonConfig(**config_data)
            return config
        except ValidationError as e:
            raise ValueError(f"Configuration validation failed: {e}")

    @staticmethod
    def load_from_env() -> ArkhonConfig:
        # Stub for env var loading logic
        # In real impl, we would map ARKHON_LLM_MODEL -> llm.model etc.
        # For now, just return default
        return ArkhonConfig()
