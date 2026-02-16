from typing import Any, Optional, Dict
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.core.nodes.base import BaseNode


class ThoughtNode(BaseNode):
    """
    Node responsible for generating thoughts using an LLM.
    """

    def __init__(self, llm: Any, system_prompt: Optional[str] = None):
        """
        Initialize with a LangChain-compatible runnable (LLM or Chain).
        """
        self.llm = llm
        self.system_prompt = system_prompt

    async def execute(self, state: AgentState) -> AgentState:
        """
        Generate a thought based on the current state.
        """
        # Prepare context from messages
        messages = state.get("messages", [])

        # Invoke LLM (assuming it might be sync or async, but typically we wrap in a Runnable)
        # For simplicity in this refactor, we maintain sync invoke if used, but wrap in awaitable if possible.
        # In a real LangGraph setup, this node typically interacts with a bound LLM.

        response = self.llm.invoke(messages)

        # Handle response types (Str or AIMessage)
        content = response
        if hasattr(response, "content"):
            content = response.content

        # Append new message to history
        new_message = {"role": "assistant", "content": str(content)}
        state["messages"].append(new_message)

        return state
