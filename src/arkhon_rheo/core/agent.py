"""Agent Core Module.

This module defines the abstract base class for all agents in the multi-agent system,
providing basic message passing and asynchronous execution mechanisms.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arkhon_rheo.core.message import AgentMessage


class Agent(ABC):
    """Abstract base class for all agents in the multi-agent system.

    Encapsulates basic agent properties including an inbox (Queue), name,
    and fundamental communication methods. Each instance automatically
    registers itself with the AgentRegistry upon initialization.

    Attributes:
        name: Unique identifier for the agent.
        inbox: Asynchronous queue for receiving messages.
    """

    def __init__(self, name: str) -> None:
        """Initialize the Agent instance.

        Args:
            name: The name of the agent, must be unique in the Registry.
        """
        self.name = name
        self.inbox: asyncio.Queue[AgentMessage] = asyncio.Queue()

        # Auto-register
        from arkhon_rheo.core.registry import AgentRegistry  # noqa: PLC0415

        AgentRegistry.register(self)

    async def send_message(self, recipient: "Agent", message: "AgentMessage") -> None:
        """Send a message to another agent.

        Args:
            recipient: The target agent instance to receive the message.
            message: The message object to be sent.
        """
        await recipient.inbox.put(message)

    async def _resolve_agent(self, name: str) -> "Agent | None":
        """Resolve an agent instance by its name.

        Internal method that utilizes AgentRegistry to find the specified agent.

        Args:
            name: The name of the target agent.

        Returns:
            The agent instance if found, otherwise None.
        """
        from arkhon_rheo.core.registry import AgentRegistry  # noqa: PLC0415

        return AgentRegistry.get(name)

    async def receive_message(self) -> "AgentMessage":
        """Wait for and retrieve the next message from the inbox.

        Returns:
            The retrieved AgentMessage object.
        """
        return await self.inbox.get()

    @abstractmethod
    async def process_message(self, message: "AgentMessage") -> None:
        """Process an incoming message.

        Abstract method that must be implemented by subclasses to define
        specific business logic.

        Args:
            message: The message object to be processed.
        """
        pass

    async def run(self) -> None:
        """Main execution loop for the agent.

        Continuously retrieves messages from the inbox and calls
        process_message to handle them.
        """
        while True:
            message = await self.receive_message()
            await self.process_message(message)
