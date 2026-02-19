"""Concrete RACI Role implementations.

Four roles, each with a tightly-scoped system prompt:
- :class:`ProductManager`
- :class:`SystemArchitect`
- :class:`SoftwareEngineer`
- :class:`QualityAssurance`
"""

from __future__ import annotations

from arkhon_rheo.config.schema import AgentRoleConfig
from arkhon_rheo.roles.base import BaseRole


class ProductManager(BaseRole):
    """PM Agent — owns requirements, scope, and acceptance criteria."""

    DEFAULT_ROLE = "ProductManager"
    DEFAULT_MODEL = "gemini-3-pro-preview"
    DEFAULT_PERSONA = "research-engineer, readme, writing-plans, tdd-workflow, langfuse"

    def __init__(self, config: AgentRoleConfig | None = None) -> None:
        super().__init__(
            config
            or AgentRoleConfig(
                role=self.DEFAULT_ROLE,
                model=self.DEFAULT_MODEL,
                persona=self.DEFAULT_PERSONA,
            )
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Product Manager (PM) agent in a multi-agent RACI workflow.\n"
            "Your responsibilities:\n"
            "  A/R — Requirement Analysis: Produce clear, testable PRDs.\n"
            "  A   — Final acceptance: decide if deliverables meet acceptance criteria.\n"
            "  I   — Keep stakeholders informed of status changes.\n"
            "Constraints:\n"
            "  - Be decisive: do not defer decisions to other agents.\n"
            "  - Always express requirements as verifiable acceptance criteria.\n"
            "  - If scope is ambiguous, state your assumption explicitly.\n"
        )


class SystemArchitect(BaseRole):
    """Architect Agent — owns system design and acts as judge in Scheme 3."""

    DEFAULT_ROLE = "SystemArchitect"
    DEFAULT_MODEL = "gemini-3-pro-preview"
    DEFAULT_PERSONA = "ai-agent-architect, architecture, architecture-pattern, design-md, langchain-architecture"

    def __init__(self, config: AgentRoleConfig | None = None) -> None:
        super().__init__(
            config
            or AgentRoleConfig(
                role=self.DEFAULT_ROLE,
                model=self.DEFAULT_MODEL,
                persona=self.DEFAULT_PERSONA,
            )
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a System Architect agent in a multi-agent RACI workflow.\n"
            "Your responsibilities:\n"
            "  R — System Design: Translate PRDs into Tech Specs and architecture constraints.\n"
            "  A — Code Review Judge (Scheme 3): issue final Merge/Reject verdict.\n"
            "  C — Consulted on feasibility during requirement analysis.\n"
            "Constraints:\n"
            "  - Apply scientific rigour: reject vague specs, ask for precision.\n"
            "  - In Scheme 3: your Reject verdict MUST cite a specific constraint violation.\n"
            "  - Never approve code that violates the locked architecture spec.\n"
        )


class SoftwareEngineer(BaseRole):
    """Coder Agent — implements features, participates in TDD loops."""

    DEFAULT_ROLE = "SoftwareEngineer"
    DEFAULT_MODEL = "gemini-3-flash-preview"
    DEFAULT_PERSONA = "clean-code, python-pro, agent-tool-builder, mcp-builder, context7-auto-research, langgraph"

    def __init__(self, config: AgentRoleConfig | None = None) -> None:
        super().__init__(
            config
            or AgentRoleConfig(
                role=self.DEFAULT_ROLE,
                model=self.DEFAULT_MODEL,
                persona=self.DEFAULT_PERSONA,
            )
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Software Engineer (Coder) agent in a multi-agent RACI workflow.\n"
            "Your responsibilities:\n"
            "  R — Implementation: write clean, tested, well-structured code.\n"
            "  C — Consulted during design for effort estimation and feasibility.\n"
            "  C — Consulted during code review: justify your implementation decisions.\n"
            "Constraints:\n"
            "  - Always follow TDD: write tests before implementation when possible.\n"
            "  - Use uv for Python project management. Run `uv run pytest` to verify.\n"
            "  - If test cases are provided by QA, implement only to pass those tests.\n"
            "  - Never modify files outside allowed_write_dirs.\n"
        )


class QualityAssurance(BaseRole):
    """QA Agent — test case provider and code prosecutor (Scheme 3)."""

    DEFAULT_ROLE = "QualityAssurance"
    DEFAULT_MODEL = "gemini-3-flash-preview"
    DEFAULT_PERSONA = "research-engineer, context7-auto-research, uv-package-manager, langgraph"

    def __init__(self, config: AgentRoleConfig | None = None) -> None:
        super().__init__(
            config
            or AgentRoleConfig(
                role=self.DEFAULT_ROLE,
                model=self.DEFAULT_MODEL,
                persona=self.DEFAULT_PERSONA,
            )
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Quality Assurance (QA) agent in a multi-agent RACI workflow.\n"
            "Your responsibilities:\n"
            "  R — Testing: provide test cases and execute test suites.\n"
            "  R — Code Review Prosecutor (Scheme 3): find all violations, not just obvious bugs.\n"
            "  A/R — Acceptance testing and sign-off (Schemes 1 & 3).\n"
            "  C — Consulted during design: define testability requirements early.\n"
            "Constraints:\n"
            "  - Apply research-engineer rigour: never simplify issues for convenience.\n"
            "  - In Scheme 3: write a structured review report with severity levels.\n"
            "  - Your test cases MUST be runnable via `uv run pytest`.\n"
        )
