"""Action Node Module.

This module provides the ActionNode class, which is responsible for executing
external tools or actions based on tool calls requested by an LLM.

Security hardening (2026-02-20):
- Tool arguments are validated before execution (type, allowed keys).
- Argument values are constrained to JSON-safe scalar/container types.
- Argument strings are length-capped to prevent oversized payloads.
"""

from __future__ import annotations

import logging
from typing import Any

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode

_log = logging.getLogger(__name__)

# Maximum length of any single string argument value supplied by the LLM.
_MAX_ARG_STR_LEN = 4096

# JSON-safe scalar types accepted as argument values.
_SCALAR_TYPES = (str, int, float, bool, type(None))


def _validate_args(tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
    """Validate and sanitise LLM-supplied tool arguments.

    Rules:
    - ``args`` must be a plain ``dict``.
    - Keys must be non-empty strings.
    - Values must be JSON-safe scalars or lists/dicts composed of them.
    - String values are truncated to ``_MAX_ARG_STR_LEN`` characters.

    Args:
        tool_name: Name of the tool (used in error messages).
        args: Raw argument dict from the LLM.

    Returns:
        Sanitised copy of *args*.

    Raises:
        TypeError: If *args* is not a dict or contains invalid types.
        ValueError: If a key is empty or a value fails validation.
    """
    if not isinstance(args, dict):
        raise TypeError(f"Tool '{tool_name}': args must be a dict, got {type(args).__name__}")

    clean: dict[str, Any] = {}
    for key, value in args.items():
        if not isinstance(key, str) or not key:
            raise ValueError(f"Tool '{tool_name}': invalid arg key {key!r}")
        clean[key] = _sanitize_value(tool_name, key, value, depth=0)
    return clean


def _sanitize_value(tool_name: str, key: str, value: Any, depth: int) -> Any:
    """Recursively sanitise a single argument value."""
    if depth > 4:
        raise ValueError(f"Tool '{tool_name}': arg '{key}' is nested too deeply.")
    if isinstance(value, str):
        if len(value) > _MAX_ARG_STR_LEN:
            _log.warning(
                "arg_truncated",
                extra={"tool": tool_name, "key": key, "original_len": len(value)},
            )
            return value[:_MAX_ARG_STR_LEN]
        return value
    if isinstance(value, _SCALAR_TYPES):
        return value
    if isinstance(value, list):
        return [_sanitize_value(tool_name, key, v, depth + 1) for v in value]
    if isinstance(value, dict):
        return {k: _sanitize_value(tool_name, k, v, depth + 1) for k, v in value.items() if isinstance(k, str)}
    raise TypeError(f"Tool '{tool_name}': arg '{key}' has unsupported type {type(value).__name__}")


class ActionNode(BaseNode):
    """Node responsible for executing actions (tools).

    The ActionNode inspects the last message for tool calls, validates the
    LLM-supplied arguments, executes the corresponding tools, and appends
    the results back to the AgentState.

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
            tool_name = tool_call.get("name", "")
            raw_args = tool_call.get("args", {})
            tool_id = tool_call.get("id")

            tool = self.tools.get(tool_name)

            if not tool:
                result = f"Error: Tool '{tool_name}' not found."
            else:
                try:
                    tool_args = _validate_args(tool_name, raw_args)
                    # Support both callable and .run() interface
                    if hasattr(tool, "run"):
                        result = tool.run(**tool_args)
                    elif callable(tool):
                        result = tool(**tool_args)
                    else:
                        result = f"Error: Tool '{tool_name}' is not executable."
                except (TypeError, ValueError) as exc:
                    _log.warning(
                        "tool_arg_validation_failed",
                        extra={"tool": tool_name, "error": str(exc)},
                    )
                    result = f"Error: Invalid arguments for '{tool_name}': {exc}"
                except Exception as e:
                    result = f"Error executing '{tool_name}': {e!s}"

            # Append tool result to messages
            state["messages"].append({"role": "tool", "content": str(result), "tool_call_id": tool_id})

        return state
