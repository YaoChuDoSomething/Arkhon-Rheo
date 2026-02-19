"""Coordinator Agent Module.

This module provides the CoordinatorAgent class, which acts as a central hub
for routing messages between users and specialist agents based on intent.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class CoordinatorAgent(Agent):
    """Agent responsible for routing tasks to specialist agents based on intent.

    The CoordinatorAgent maintains a routing table mapping specific intents
    to specialist agents. It facilitates nested or distributed workflows
    by forwarding requests and returning responses to original requesters.

    Attributes:
        routing_table: A dictionary mapping intent strings to Agent instances.
    """

    def __init__(self, name: str) -> None:
        """Initialize a CoordinatorAgent instance.

        Args:
            name: The unique name of the agent.
        """
        super().__init__(name)
        self.routing_table: dict[str, Agent] = {}

    def register_agent(self, intent: str, agent: Agent) -> None:
        """Register a specialist agent for a specific intent.

        Args:
            intent: The intent string (e.g., "calculate", "search").
            agent: The Agent instance to handle this intent.
        """
        self.routing_table[intent] = agent

    async def route_task(self, intent: str) -> Agent | None:
        """Find the agent responsible for the given intent.

        Args:
            intent: The intent to resolve.

        Returns:
            The Agent instance if a route exists, otherwise None.
        """
        return self.routing_table.get(intent)

    async def process_message(self, message: AgentMessage) -> None:
        """Process incoming request or response messages for routing.

        Coordinates the forwarding of requests to specialist agents and the
        return of responses back to original senders based on message metadata.

        Args:
            message: The AgentMessage to process.
        """
        if message.type == "request":
            intent = message.metadata.get("intent")
            if not intent:
                logger.warning(
                    f"Coordinator {self.name}: Missing intent in request {message.id}"
                )
                return

            target_agent = await self.route_task(intent)
            if target_agent:
                # Add reply_to metadata so the response can be routed back
                metadata = message.metadata.copy()
                metadata["reply_to"] = message.sender

                forwarded_msg = AgentMessage(
                    sender=self.name,
                    receiver=target_agent.name,
                    content=message.content,
                    type="request",
                    correlation_id=message.id,
                    metadata=metadata,
                )
                await self.send_message(target_agent, forwarded_msg)
            else:
                logger.warning(
                    f"Coordinator {self.name}: No route found for intent '{intent}'"
                )

        elif message.type == "response":
            # Forward response back to the original requester
            reply_to = message.metadata.get("reply_to")
            if reply_to:
                # Resolve recipient using Registry (via _resolve_agent helper or Registry directly)
                from arkhon_rheo.core.registry import AgentRegistry

                # Registry is usually accessed via instance in singleton pattern
                # Assuming AgentRegistry.get is a static/class method or accessible via singleton
                registry = AgentRegistry()
                target_agent = registry.get(reply_to)

                if target_agent:
                    forwarded_msg = AgentMessage(
                        sender=self.name,
                        receiver=target_agent.name,
                        content=message.content,
                        type="response",
                        correlation_id=message.correlation_id,
                        metadata=message.metadata,
                    )
                    await self.send_message(target_agent, forwarded_msg)
                else:
                    logger.warning(
                        f"Coordinator {self.name}: Target '{reply_to}' not found for response forwarding"
                    )
            else:
                logger.debug(
                    f"Coordinator {self.name}: Response received without 'reply_to' metadata"
                )
