"""BaseRole — Abstract foundation for all RACI agent roles.

Each role wraps a LangChain-compatible chat model and exposes:
- ``system_prompt``: persona-driven system instructions
- ``invoke()``: runs the model with the current message history
- ``persona_list``: the skill names composing this role
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

import structlog
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from arkhon_rheo.config.schema import AgentRoleConfig

logger = structlog.get_logger(__name__)


class BaseRole(ABC):
    """Abstract base for RACI agent roles.

    Subclasses must implement :meth:`system_prompt`.

    Attributes:
        config: The :class:`AgentRoleConfig` governing this role.
        llm: The underlying LangChain chat model.
    """

    def __init__(self, config: AgentRoleConfig) -> None:
        self.config = config
        self.llm = ChatGoogleGenerativeAI(
            model=config.model,
            temperature=0.4,
        )
        self._log = logger.bind(role=config.role, model=config.model)

    # ------------------------------------------------------------------
    # Subclass contract
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the role-specific system instruction string."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def persona_list(self) -> list[str]:
        """Return the skill names composing this role's persona."""
        return self.config.persona_list

    def invoke(
        self,
        user_content: str,
        history: list[dict[str, Any]] | None = None,
    ) -> str:
        """Run the LLM for this role.

        Args:
            user_content: The prompt or question to process.
            history: Optional prior message dicts with ``role`` / ``content`` keys.

        Returns:
            The model's text response.
        """
        messages: list = [SystemMessage(content=self._full_system_prompt())]

        for msg in history or []:
            role = msg.get("role", "human")
            content = msg.get("content", "")
            if role == "ai":
                messages.append(AIMessage(content=content))
            else:
                messages.append(HumanMessage(content=content))

        messages.append(HumanMessage(content=user_content))

        t0 = time.perf_counter()
        response = self.llm.invoke(messages)
        elapsed = time.perf_counter() - t0

        text: str = response.content if isinstance(response.content, str) else str(response.content)
        self._log.info("invoke_complete", elapsed_s=round(elapsed, 3), tokens=len(text.split()))
        return text

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _full_system_prompt(self) -> str:
        persona_block = f"\nActive skill personas: {', '.join(self.persona_list)}" if self.persona_list else ""
        return self.system_prompt + persona_block
