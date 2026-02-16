from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    model: str = Field(default="gemini-2.0-flash", description="Model name to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1024, gt=0)
    api_key: Optional[str] = Field(
        default=None, description="API Key (optional, prefer env vars)"
    )


class ToolConfig(BaseModel):
    enabled_tools: List[str] = Field(
        default_factory=list, description="List of enabled tool names"
    )
    tool_kwargs: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Per-tool configuration"
    )


class RuleConfig(BaseModel):
    max_steps: int = Field(default=10, gt=0)
    forbid_guessing: bool = Field(default=True)
    cost_limit: float = Field(default=1.0, gt=0.0)


class SystemConfig(BaseModel):
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")


class ArkhonConfig(BaseModel):
    llm: LLMConfig = Field(default_factory=LLMConfig)
    tools: ToolConfig = Field(default_factory=ToolConfig)
    rules: RuleConfig = Field(default_factory=RuleConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
