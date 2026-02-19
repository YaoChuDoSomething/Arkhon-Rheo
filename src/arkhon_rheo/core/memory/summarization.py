"""Summarization Module.

This module provides the Summarizer class, which handles context compression
by using an LLM to summarize a sequence of messages, helping to manage
token limits and maintain focus in long conversations.
"""

from __future__ import annotations

from typing import Any


class Summarizer:
    """Handles context compression using an LLM.

    The summarizer converts a list of messages into a concise summary,
    preserving key facts and entities while reducing the overall token count.

    Attributes:
        llm_client: The LLM client used to perform the summarization.
    """

    def __init__(self, llm_client: Any) -> None:
        """Initialize a Summarizer instance.

        Args:
            llm_client: An instance of an LLM client (e.g., Google GenAI Client).
        """
        self.llm_client = llm_client

    async def summarize(self, messages: list[dict[str, Any]]) -> str:
        """Summarize a list of messages into a single string.

        Args:
            messages: A list of message dictionaries to summarize.

        Returns:
            A string containing the summary of the conversation.
        """
        if not messages:
            return ""

        lines = [
            "Summarize the following conversation history, preserving all key facts and entities:\n"
        ]
        for msg in messages:
            lines.append(f"{msg['role']}: {msg['content']}")

        prompt = "\n".join(lines)

        # Call LLM (assuming the client supports the necessary methods)
        if hasattr(self.llm_client, "generate_content_async"):
            response = await self.llm_client.generate_content_async(prompt)
        else:
            # Fallback for sync clients
            response = self.llm_client.generate_content(prompt)
        return response.text
