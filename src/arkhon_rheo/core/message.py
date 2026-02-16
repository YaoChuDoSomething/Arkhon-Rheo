from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Dict
import json
import uuid


@dataclass
class AgentMessage:
    """
    Standard message format for agent communication.
    """

    sender: str
    receiver: str
    content: Any
    type: str  # "request", "response", "notification"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Serialize message to JSON string."""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> "AgentMessage":
        """Deserialize message from JSON string."""
        data = json.loads(json_str)
        return cls(**data)
