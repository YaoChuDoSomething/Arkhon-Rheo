"""Specialist Agent Module.

This module provides the SpecialistAgent class, which implements domain-specific
logic for processing requests and generating expert responses.
"""

from __future__ import annotations

import logging

from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage

logger = logging.getLogger(__name__)


class SpecialistAgent(Agent):
    """Agent specialized in a specific domain.

    The SpecialistAgent handles expert tasks within its assigned domain
    (e.g., math, research) and communicates results back to the requester.

    Attributes:
        domain: The specialized field of expertise for this agent.
    """

    def __init__(self, name: str, domain: str) -> None:
        """Initialize a SpecialistAgent instance.

        Args:
            name: The unique name of the agent.
            domain: The domain of expertise (e.g., "physics", "code").
        """
        super().__init__(name)
        self.domain = domain

    async def process_message(self, message: AgentMessage) -> None:
        """Process an incoming request and generate a domain-specific result.

        Args:
            message: The request AgentMessage to process.
        """
        if message.type == "request":
            # Simulate domain-specific processing
            result = f"Processed by {self.domain} specialist: {message.content}"

            # Create the response message
            reply = AgentMessage(
                sender=self.name,
                receiver=message.sender,
                content=result,
                type="response",
                correlation_id=message.id,
                metadata=message.metadata,
            )

            # Resolve recipient via Registry to ensure proper routing
            from arkhon_rheo.core.registry import AgentRegistry

            registry = AgentRegistry()
            recipient_agent = registry.get(message.sender)

            if recipient_agent:
                await self.send_message(recipient_agent, reply)
            else:
                logger.error(
                    f"Specialist '{self.name}' could not find recipient '{message.sender}' in registry."
                )
