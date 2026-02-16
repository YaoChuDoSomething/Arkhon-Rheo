import pytest
import yaml
from arkhon_rheo.config.schema import ArkhonConfig
from arkhon_rheo.config.loader import ConfigLoader


def test_default_config():
    config = ArkhonConfig()
    assert config.llm.model == "gemini-2.0-flash"
    assert config.rules.max_steps == 10


def test_valid_yaml_loading(tmp_path):
    config_file = tmp_path / "config.yaml"
    data = {
        "llm": {"model": "gemini-pro", "temperature": 0.5},
        "rules": {"max_steps": 20},
    }
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    loader = ConfigLoader(str(config_file))
    config = loader.load()

    assert config.llm.model == "gemini-pro"
    assert config.llm.temperature == 0.5
    assert config.rules.max_steps == 20
    assert config.system.debug is False  # Default


def test_invalid_config_validation(tmp_path):
    config_file = tmp_path / "invalid.yaml"
    data = {
        "llm": {"temperature": 2.0}  # Invalid > 1.0
    }
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    loader = ConfigLoader(str(config_file))
    with pytest.raises(ValueError) as exc:
        loader.load()
    assert "validation failed" in str(exc.value)


def test_missing_file():
    loader = ConfigLoader("nonexistent.yaml")
    with pytest.raises(FileNotFoundError):
        loader.load()
