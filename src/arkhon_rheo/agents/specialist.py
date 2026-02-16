from typing import Dict
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class SpecialistAgent(Agent):
    """
    Agent specialized in a specific domain.
    """

    def __init__(self, name: str, domain: str):
        super().__init__(name)
        self.domain = domain

    async def process_message(self, message: AgentMessage) -> None:
        """
        Process incoming tasks.
        """
        if message.type == "request":
            # Simulate work
            result = f"Processed by {self.domain} specialist: {message.content}"

            # Send response
            reply = AgentMessage(
                sender=self.name,
                receiver=message.sender,
                content=result,
                type="response",
                correlation_id=message.id,
                metadata=message.metadata,
            )

            # Resolve recipient via directory for proper typing
            # Using Registry via base class
            from arkhon_rheo.core.registry import AgentRegistry

            recipient_agent = AgentRegistry.get(message.sender)

            if recipient_agent:
                await self.send_message(recipient_agent, reply)
            else:
                # If recipient not in registry, meaningful error or log
                pass
