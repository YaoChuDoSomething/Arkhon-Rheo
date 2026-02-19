"""Thought Node Module.

This module provides the ThoughtNode class, which is responsible for
generating reasoning steps or internal "thoughts" using an LLM within the
agentic graph.
"""

from __future__ import annotations

from typing import Any

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class ThoughtNode(BaseNode):
    """Node responsible for generating thoughts via an LLM.

    The ThoughtNode takes the current messages from the AgentState, invokes
    an LLM to generate a reasoning response, and appends that response back
    to the state's message history.

    Attributes:
        llm: A LangChain-compatible runnable (LLM or Chain) for inference.
        system_prompt: Optional prompt to guide the LLM's reasoning style.
    """

    def __init__(self, llm: Any, system_prompt: str | None = None) -> None:
        """Initialize a ThoughtNode instance.

        Args:
            llm: An LLM client or chain capable of receiving message history.
            system_prompt: Optional system-level instructions for the LLM.
        """
        super().__init__()
        self.llm = llm
        self.system_prompt = system_prompt

    async def execute(self, state: AgentState) -> AgentState:
        """Generate a thought based on the current conversation history.

        Args:
            state: The incoming AgentState.

        Returns:
            The AgentState containing the newly generated thought message.
        """
        # Prepare context from messages
        messages = state.get("messages", [])

        # Invoke LLM
        # Note: In a production setting, this would typically involve async invocation.
        response = self.llm.invoke(messages)

        # Handle response types (Str or AIMessage-like objects)
        content = response
        if hasattr(response, "content"):
            content = response.content

        # Append new message to history
        new_message = {"role": "assistant", "content": str(content)}
        if "messages" not in state:
            state["messages"] = []
        state["messages"].append(new_message)

        return state
