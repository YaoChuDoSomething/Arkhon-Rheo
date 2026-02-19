"""Execution Context Module.

This module provides a ContextManager to handle execution context, such as
trace IDs and user information, using contextvars to ensure isolation
between threads and asynchronous tasks.
"""

import uuid
from contextvars import ContextVar
from typing import Any


class ContextManager:
    """Manages execution context using contextvars.

    Ensures that contextual data remains isolated between concurrent
    asynchronous tasks or threads.
    """

    _context: ContextVar[dict[str, Any]] = ContextVar("arkhon_context", default={})

    def get_context(self) -> dict[str, Any]:
        """Return a copy of the current context dictionary.

        Returns:
            A dictionary containing the current context items.
        """
        return self._context.get().copy()

    def set(self, key: str, value: Any) -> None:
        """Set a value in the current context.

        Args:
            key: The context key to set.
            value: The value to associate with the key.
        """
        ctx = self.get_context()
        ctx[key] = value
        self._context.set(ctx)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the current context.

        Args:
            key: The context key to retrieve.
            default: The value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value.
        """
        return self._context.get().get(key, default)

    def clear(self) -> None:
        """Clear the current context dictionary."""
        self._context.set({})

    def init_trace(self) -> str:
        """Initialize a new trace ID in the context if one does not exist.

        Returns:
            The newly generated trace ID string.
        """
        trace_id = str(uuid.uuid4())
        self.set("trace_id", trace_id)
        return trace_id
