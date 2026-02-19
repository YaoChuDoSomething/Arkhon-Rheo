"""Configuration Schema Module.

This module defines the Pydantic models used to represent and validate the
Arkhon-Rheo framework's configuration hierarchy.
Includes RACI workflow config extension (RACIWorkflowConfig).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """Configuration for Large Language Model clients."""

    model: str = Field(default="gemini-2.0-flash", description="Model name to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1024, gt=0)
    api_key: str | None = Field(default=None, description="API Key (optional, prefer env vars)")


class ToolConfig(BaseModel):
    """Configuration for tool enablement and per-tool settings."""

    enabled_tools: list[str] = Field(default_factory=list, description="List of enabled tool names")
    tool_kwargs: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Per-tool configuration parameters"
    )


class RuleConfig(BaseModel):
    """Configuration for governance rules and execution constraints."""

    max_steps: int = Field(default=10, gt=0)
    forbid_guessing: bool = Field(default=True)
    cost_limit: float = Field(default=1.0, gt=0.0)


class SystemConfig(BaseModel):
    """General system-level settings."""

    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")


# ---------------------------------------------------------------------------
# RACI Workflow Config Models
# ---------------------------------------------------------------------------


class WorkflowScheme(StrEnum):
    """Available RACI workflow orchestration schemes."""

    WATERFALL = "waterfall"
    AGILE = "agile"
    CRITIC = "critic"
    AGENT_EVALUATION = "agent-evaluation"


class AgentRoleConfig(BaseModel):
    """Configuration for a single RACI agent role.

    Attributes:
        role: PascalCase class name identifier (e.g. 'ProductManager').
        model: LLM model name to use for this role.
        persona: Comma-separated skill names that compose this role's persona.
    """

    role: str
    model: str = Field(default="gemini-3-flash-preview")
    persona: str = Field(default="research-engineer")

    @property
    def persona_list(self) -> list[str]:
        """Return persona as a list of trimmed skill names."""
        return [p.strip() for p in self.persona.split(",") if p.strip()]


class ConstraintsConfig(BaseModel):
    """Operational constraints for the target project tool."""

    allowed_write_dirs: list[str] = Field(
        default=["src/", "tests/", "docs/"],
        description="Directories agent is allowed to write into.",
    )
    shell_whitelist: list[str] = Field(
        default=["uv run pytest", "ruff check", "ty check"],
        description="Shell commands agent is allowed to execute.",
    )
    auto_commit: bool = Field(
        default=False,
        description="If True, agent may commit changes automatically.",
    )


class TargetProjectConfig(BaseModel):
    """Configuration for the DEV-TARGET project the agents operate on."""

    name: str = Field(default="", description="Human-readable project name.")
    target_path: str = Field(default="../dlamp", description="Relative or absolute path.")


class OrchestrationConfig(BaseModel):
    """Meta-orchestration settings."""

    default_scheme: WorkflowScheme = Field(default=WorkflowScheme.AGENT_EVALUATION)
    constraints: ConstraintsConfig = Field(default_factory=ConstraintsConfig)


class MemoryConfig(BaseModel):
    """Agent memory architecture settings."""

    project_rag_enabled: bool = Field(default=True)
    episode_log_path: str = Field(default="./.agent/episodes.json")


class AgentsConfig(BaseModel):
    """Named agent role definitions keyed by shorthand (pm/architect/coder/qa)."""

    pm: AgentRoleConfig = Field(default_factory=lambda: AgentRoleConfig(role="ProductManager"))
    architect: AgentRoleConfig = Field(default_factory=lambda: AgentRoleConfig(role="SystemArchitect"))
    coder: AgentRoleConfig = Field(default_factory=lambda: AgentRoleConfig(role="SoftwareEngineer"))
    qa: AgentRoleConfig = Field(default_factory=lambda: AgentRoleConfig(role="QualityAssurance"))


class RACIWorkflowConfig(BaseModel):
    """Top-level RACI workflow configuration parsed from config/workflow_context.yaml."""

    project: TargetProjectConfig = Field(default_factory=TargetProjectConfig)
    agents: AgentsConfig = Field(default_factory=AgentsConfig)
    orchestration: OrchestrationConfig = Field(default_factory=OrchestrationConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)


# ---------------------------------------------------------------------------
# Framework Root Config
# ---------------------------------------------------------------------------


class ArkhonConfig(BaseModel):
    """Root configuration model for the Arkhon-Rheo framework."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    tools: ToolConfig = Field(default_factory=ToolConfig)
    rules: RuleConfig = Field(default_factory=RuleConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
