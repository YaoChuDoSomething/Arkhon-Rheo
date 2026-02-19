"""Context Window Module.

This module provides the ContextWindow class, which implements a sliding
window for conversation history management, ensuring the total token count
remains within specified limits.
"""

from __future__ import annotations

from typing import Any


class ContextWindow:
    """Implements a sliding window for context management.

    Maintains a list of recent messages and automatically evicts the oldest
    entries when the total token count exceeds a predefined maximum.

    Attributes:
        max_tokens: The maximum number of tokens allowed in the window.
        messages: A list of message dictionaries currently in the window.
        current_tokens: The current cumulative token count of all messages.
    """

    def __init__(self, max_tokens: int) -> None:
        """Initialize a ContextWindow instance.

        Args:
            max_tokens: The token limit for this context window.
        """
        self.max_tokens = max_tokens
        self.messages: list[dict[str, Any]] = []
        self.current_tokens = 0

    def add_message(self, role: str, content: str, tokens: int) -> None:
        """Add a message to the window and maintain the token limit.

        If adding the message causes the token count to exceed max_tokens,
        older messages are removed until the count is within limits.

        Args:
            role: The role attributed to the message (e.g., "user", "assistant").
            content: The textual content of the message.
            tokens: The estimated token count for this message.
        """
        self.messages.append({"role": role, "content": content, "tokens": tokens})
        self.current_tokens += tokens

        # Evict oldest messages if exceeding limit
        while self.current_tokens > self.max_tokens and self.messages:
            removed = self.messages.pop(0)
            self.current_tokens -= removed["tokens"]
