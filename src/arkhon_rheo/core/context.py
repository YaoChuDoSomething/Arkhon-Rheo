import uuid
from contextvars import ContextVar
from typing import Any, Dict, Optional


class ContextManager:
    """
    Manages execution context (trace IDs, user info) using contextvars.
    Ensures isolation between threads and async tasks.
    """

    _context: ContextVar[Dict[str, Any]] = ContextVar("arkhon_context", default={})

    def get_context(self) -> Dict[str, Any]:
        """Return a copy of the current context dictionary."""
        return self._context.get().copy()

    def set(self, key: str, value: Any) -> None:
        """Set a value in the current context."""
        ctx = self.get_context()
        ctx[key] = value
        self._context.set(ctx)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the current context."""
        return self._context.get().get(key, default)

    def clear(self) -> None:
        """Clear the current context."""
        self._context.set({})

    def init_trace(self) -> str:
        """Initialize a new trace ID if one doesn't exist."""
        trace_id = str(uuid.uuid4())
        self.set("trace_id", trace_id)
        return trace_id
