import uuid
from typing import Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ContextManager:
    """
    Manages execution context including trace IDs and metadata.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add or update a metadata entry."""
        self._metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Retrieve a metadata entry."""
        return self._metadata.get(key, default)

    def get_all_metadata(self) -> Dict[str, Any]:
        """Return a copy of all metadata, including system fields."""
        return {
            "trace_id": self.trace_id,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            **self._metadata,
        }

    def new_trace(self) -> str:
        """Generate a new trace ID for a new execution path."""
        self.trace_id = str(uuid.uuid4())
        return self.trace_id
