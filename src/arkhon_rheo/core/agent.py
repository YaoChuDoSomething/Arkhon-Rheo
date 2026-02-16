from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Optional
from arkhon_rheo.core.message import AgentMessage


class Agent(ABC):
    """
    Base class for all agents in the multi-agent system.
    """

    def __init__(self, name: str):
        self.name = name
        self.inbox: asyncio.Queue[AgentMessage] = asyncio.Queue()
        # Auto-register
        from arkhon_rheo.core.registry import AgentRegistry

        AgentRegistry.register(self)

    async def send_message(self, recipient: "Agent", message: AgentMessage) -> None:
        """
        Send a message to another agent.
        """
        await recipient.inbox.put(message)

    async def _resolve_agent(self, name: str) -> Optional["Agent"]:
        """Resolve agent by name using the Registry."""
        from arkhon_rheo.core.registry import AgentRegistry

        return AgentRegistry.get(name)

    async def receive_message(self) -> AgentMessage:
        """
        Wait for and retrieve the next message from the inbox.
        """
        return await self.inbox.get()

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> None:
        """
        Process an incoming message. Must be implemented by subclasses.
        """
        pass

    async def run(self) -> None:
        """
        Main loop for the agent to process messages.
        """
        while True:
            message = await self.receive_message()
            await self.process_message(message)
