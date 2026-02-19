"""Action Node Module.

This module provides the ActionNode class, which is responsible for executing
external tools or actions based on tool calls requested by an LLM.
"""

from __future__ import annotations

from typing import Any

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class ActionNode(BaseNode):
    """Node responsible for executing actions (tools).

    The ActionNode inspects the last message for tool calls, executes the
    corresponding tools using provided arguments, and appends the results
    back to the AgentState.

    Attributes:
        tools: A dictionary mapping tool names to their implementations.
    """

    def __init__(self, tools: dict[str, Any]) -> None:
        """Initialize an ActionNode instance.

        Args:
            tools: A mapping of tool names to callable objects or tool instances.
        """
        super().__init__()
        self.tools = tools

    async def execute(self, state: AgentState) -> AgentState:
        """Execute tool calls found in the message history.

        Args:
            state: The incoming AgentState.

        Returns:
            The AgentState containing the tool results as new messages.
        """
        messages = state.get("messages", [])
        if not messages:
            return state

        last_message = messages[-1]
        tool_calls = last_message.get("tool_calls", [])

        if not tool_calls:
            return state

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            tool_id = tool_call.get("id")

            tool = self.tools.get(tool_name)

            if not tool:
                result = f"Error: Tool '{tool_name}' not found."
            else:
                try:
                    # Support both callable and .run() interface
                    if hasattr(tool, "run"):
                        result = tool.run(**tool_args)
                    elif callable(tool):
                        result = tool(**tool_args)
                    else:
                        result = f"Error: Tool '{tool_name}' is not executable."
                except Exception as e:
                    result = f"Error executing '{tool_name}': {str(e)}"

            # Append tool result to messages
            state["messages"].append(
                {"role": "tool", "content": str(result), "tool_call_id": tool_id}
            )

        return state
