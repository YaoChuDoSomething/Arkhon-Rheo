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
from google import genai
from google.genai import types

from arkhon_rheo.config.schema import AgentRoleConfig

logger = structlog.get_logger(__name__)


class BaseRole(ABC):
    """Abstract base for RACI agent roles using the Google GenAI SDK.

    Subclasses must implement :meth:`system_prompt`.

    Attributes:
        config: The :class:`AgentRoleConfig` governing this role.
        client: The official Google GenAI SDK client.
    """

    def __init__(self, config: AgentRoleConfig) -> None:
        self.config = config
        self.client = genai.Client()
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
        """Run the LLM for this role using deep reasoning.

        Args:
            user_content: The prompt or question to process.
            history: Optional prior message dicts with ``role`` / ``content`` keys.

        Returns:
            The model's text response.

        Raises:
            ValueError: If ``user_content`` exceeds the maximum allowed length.
        """
        # -------------------------------------------------------------------
        # Input length guard (partial prompt-injection mitigation)
        # Overly long user inputs can be used to overflow the context window
        # or smuggle instructions across a perceived "boundary".  We cap them
        # here so the callers must make a deliberate decision to split large
        # inputs into smaller chunks.
        # -------------------------------------------------------------------
        max_input_len = 16_384  # 16 KiB
        if len(user_content) > max_input_len:
            raise ValueError(
                f"user_content exceeds maximum allowed length of {max_input_len} characters "
                f"(got {len(user_content)}). Split the input into smaller chunks."
            )
        # Build contents from history and current prompt
        # We treat the system prompt as the first system message if supported,
        # or prepend it to the first human message.
        system_instruction = self._full_system_prompt()

        contents = []
        for msg in history or []:
            role = "user" if msg.get("role") == "human" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_content)]))

        # Thinking configuration for deep reasoning (Gemini 3 and 2.5)
        model_name = self.config.model
        thinking_config = None

        if "gemini-3" in model_name:
            thinking_config = types.ThinkingConfig(thinking_level=types.ThinkingLevel.HIGH)
        elif "gemini-2.5" in model_name:
            thinking_config = types.ThinkingConfig(thinking_budget=1024)

        t0 = time.perf_counter()
        response = self.client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                thinking_config=thinking_config,
                temperature=0.4,
            ),
        )
        elapsed = time.perf_counter() - t0

        # Extract text response and log thoughts if any
        text = ""
        thoughts = []
        candidates = response.candidates
        if not candidates or not candidates[0].content:
            return text
        for part in candidates[0].content.parts or []:
            if part.thought:
                thoughts.append(part.text)
            elif part.text:
                text += part.text

        self._log.info("invoke_complete", elapsed_s=round(elapsed, 3), thoughts_count=len(thoughts), text_len=len(text))
        return text

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _full_system_prompt(self) -> str:
        persona_block = f"\nActive skill personas: {', '.join(self.persona_list)}" if self.persona_list else ""
        return self.system_prompt + persona_block
