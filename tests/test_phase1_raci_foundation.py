"""Phase 1 Unit Tests — Config Schema, RACI Loader, Roles, TargetProject."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from arkhon_rheo.config.raci_loader import load_raci_config
from arkhon_rheo.config.schema import (
    AgentRoleConfig,
    ConstraintsConfig,
    OrchestrationConfig,
    RACIWorkflowConfig,
    TargetProjectConfig,
    WorkflowScheme,
)
from arkhon_rheo.roles.concrete import (
    ProductManager,
    QualityAssurance,
    SoftwareEngineer,
    SystemArchitect,
)
from arkhon_rheo.tools.target_project import (
    ShellGuardError,
    TargetProject,
    WriteGuardError,
)

# ---------------------------------------------------------------------------
# Config Schema
# ---------------------------------------------------------------------------


class TestAgentRoleConfig:
    def test_persona_list_splits_correctly(self) -> None:
        cfg = AgentRoleConfig(role="Foo", persona="a, b, c")
        assert cfg.persona_list == ["a", "b", "c"]

    def test_persona_list_empty_string(self) -> None:
        cfg = AgentRoleConfig(role="Foo", persona="")
        assert cfg.persona_list == []


class TestWorkflowScheme:
    def test_values_are_strings(self) -> None:
        assert WorkflowScheme.WATERFALL == "waterfall"
        assert WorkflowScheme.AGENT_EVALUATION == "agent-evaluation"


class TestRACIWorkflowConfig:
    def test_defaults(self) -> None:
        cfg = RACIWorkflowConfig()
        assert cfg.project.target_path == "../dlamp"
        assert cfg.orchestration.default_scheme == WorkflowScheme.AGENT_EVALUATION
        assert cfg.orchestration.constraints.auto_commit is False

    def test_from_dict(self) -> None:
        cfg = RACIWorkflowConfig(
            project=TargetProjectConfig(name="test", target_path="../foo"),
            orchestration=OrchestrationConfig(
                default_scheme=WorkflowScheme.AGILE,
                constraints=ConstraintsConfig(auto_commit=True),
            ),
        )
        assert cfg.project.target_path == "../foo"
        assert cfg.orchestration.default_scheme == WorkflowScheme.AGILE
        assert cfg.orchestration.constraints.auto_commit is True


# ---------------------------------------------------------------------------
# RACI Loader
# ---------------------------------------------------------------------------


class TestRACILoader:
    def test_load_from_yaml(self, tmp_path: Path) -> None:
        yaml_content = textwrap.dedent(
            """
            project:
              name: "test-proj"
              target_path: "../myapp"
            agents:
              pm:
                role: "ProductManager"
                model: "gemini-3-flash-preview"
                persona: "readme, writing-plans"
            orchestration:
              default_scheme: "waterfall"
              constraints:
                auto_commit: false
            memory:
              project_rag_enabled: false
              episode_log_path: "/tmp/ep.json"
            """
        )
        config_file = tmp_path / "workflow_context.yaml"
        config_file.write_text(yaml_content, encoding="utf-8")

        cfg = load_raci_config(config_file)
        assert cfg.project.name == "test-proj"
        assert cfg.project.target_path == "../myapp"
        assert cfg.orchestration.default_scheme == WorkflowScheme.WATERFALL
        assert cfg.agents.pm.persona_list == ["readme", "writing-plans"]
        assert cfg.memory.project_rag_enabled is False

    def test_file_not_found_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_raci_config("/nonexistent/path.yaml")

    def test_bad_yaml_raises_value_error(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "bad.yaml"
        bad_file.write_text("orchestration: {default_scheme: invalid_value}", encoding="utf-8")
        # Pydantic should raise ValueError for bad enum
        with pytest.raises(ValueError):
            load_raci_config(bad_file)


# ---------------------------------------------------------------------------
# Concrete Roles — system_prompt
# ---------------------------------------------------------------------------


class TestRoleSystemPrompts:
    def test_pm_prompt_contains_requirements(self) -> None:
        assert "Requirement" in ProductManager().system_prompt

    def test_architect_prompt_contains_judge(self) -> None:
        assert "Judge" in SystemArchitect().system_prompt or "judge" in SystemArchitect().system_prompt

    def test_coder_prompt_contains_tdd(self) -> None:
        assert "TDD" in SoftwareEngineer().system_prompt

    def test_qa_prompt_contains_prosecutor(self) -> None:
        assert "Prosecutor" in QualityAssurance().system_prompt or "prosecutor" in QualityAssurance().system_prompt

    def test_roles_have_persona_list(self) -> None:
        for role in [ProductManager(), SystemArchitect(), SoftwareEngineer(), QualityAssurance()]:
            assert len(role.persona_list) > 0

    def test_config_override(self) -> None:
        custom_cfg = AgentRoleConfig(role="ProductManager", model="gemini-3-flash-preview", persona="custom-skill")
        pm = ProductManager(config=custom_cfg)
        assert pm.persona_list == ["custom-skill"]
        assert pm.config.model == "gemini-3-flash-preview"


# ---------------------------------------------------------------------------
# TargetProject — write-guards and shell-guards
# ---------------------------------------------------------------------------


class TestTargetProject:
    @pytest.fixture
    def target(self, tmp_path: Path) -> TargetProject:
        proj_cfg = TargetProjectConfig(name="test", target_path=".")
        constraints = ConstraintsConfig(
            allowed_write_dirs=["src/", "tests/"],
            shell_whitelist=["uv run pytest"],
            auto_commit=False,
        )
        return TargetProject(proj_cfg, constraints, base_dir=tmp_path)

    def test_write_allowed_path(self, target: TargetProject) -> None:
        written = target.write_file("src/hello.py", "print('hello')")
        assert written.exists()
        assert written.read_text() == "print('hello')"

    def test_write_denied_path(self, target: TargetProject) -> None:
        with pytest.raises(WriteGuardError):
            target.write_file("config/secret.yaml", "bad")

    def test_read_file(self, target: TargetProject, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "foo.py").write_text("x = 1", encoding="utf-8")
        content = target.read_file("src/foo.py")
        assert content == "x = 1"

    def test_list_files(self, target: TargetProject, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "a.py").write_text("", encoding="utf-8")
        files = target.list_files("src")
        assert "src/a.py" in files

    def test_command_denied(self, target: TargetProject) -> None:
        with pytest.raises(ShellGuardError):
            target.run_command("rm -rf /")

    def test_command_allowed_echo(self, tmp_path: Path) -> None:
        """Test with `uv run pytest --version`, which is whitelisted."""
        proj_cfg = TargetProjectConfig(name="test", target_path=".")
        constraints = ConstraintsConfig(
            allowed_write_dirs=["src/"],
            shell_whitelist=["echo"],
        )
        tp = TargetProject(proj_cfg, constraints, base_dir=tmp_path)
        output = tp.run_command("echo hello")
        assert "hello" in output
