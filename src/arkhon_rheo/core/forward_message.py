"""Forward Message pattern for multi-agent communication.

This module implements the ForwardedMessage pattern which allows sub-agent
results to bypass the supervisor synthesis step and be returned directly.
This eliminates the "telephone game" information distortion problem common
in supervisor-based multi-agent architectures.

See: multi-agent-patterns skill, Supervisor/Orchestrator section.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ForwardedMessage:
    """A sub-agent response that bypasses supervisor re-synthesis.

    When ``direct_to_user`` is ``True`` the orchestrator layer MUST pass
    the ``content`` through verbatim rather than summarising or rephrasing it.
    This preserves precision and prevents the telephone-game distortion that
    occurs when supervisors add their own interpretation at each hop.

    Attributes:
        content: The verbatim response from the sub-agent.
        source_agent: Name of the agent that produced this response.
        direct_to_user: When True, the supervisor must not paraphrase.
        metadata: Optional key/value pairs for tracing (e.g. model, tokens).
    """

    content: str
    source_agent: str
    direct_to_user: bool = True
    metadata: dict[str, str] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.content
