"""Configuration Schema Module.

This module defines the Pydantic models used to represent and validate the
Arkhon-Rheo framework's configuration hierarchy.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """Configuration for Large Language Model clients."""

    model: str = Field(default="gemini-2.0-flash", description="Model name to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1024, gt=0)
    api_key: str | None = Field(
        default=None, description="API Key (optional, prefer env vars)"
    )


class ToolConfig(BaseModel):
    """Configuration for tool enablement and per-tool settings."""

    enabled_tools: list[str] = Field(
        default_factory=list, description="List of enabled tool names"
    )
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


class ArkhonConfig(BaseModel):
    """Root configuration model for the Arkhon-Rheo framework."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    tools: ToolConfig = Field(default_factory=ToolConfig)
    rules: RuleConfig = Field(default_factory=RuleConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
