"""Agent Message Module.

This module defines the standard message format used for communication
between agents in the Arkhon-Rheo framework.
"""

import json
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AgentMessage:
    """Standard message format for agent communication.

    Attributes:
        sender: The name of the agent sending the message.
        receiver: The name of the agent intended to receive the message.
        content: The actual payload of the message.
        type: The category of the message (e.g., "request", "response", "notification").
        id: Unique identifier for the message, defaults to a new UUID.
        correlation_id: ID used to track message flows or request-response pairs.
        metadata: Additional key-value pairs for contextual information.
    """

    sender: str
    receiver: str
    content: Any
    type: str  # "request", "response", "notification"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Serialize the message instance to a JSON string.

        Returns:
            A JSON representation of the message.
        """
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> "AgentMessage":
        """Deserialize a message instance from a JSON string.

        Args:
            json_str: The JSON string to be parsed.

        Returns:
            An AgentMessage instance.
        """
        data = json.loads(json_str)
        return cls(**data)
