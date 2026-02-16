from typing import Dict, Optional
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class CoordinatorAgent(Agent):
    """
    Agent responsible for routing tasks to specialist agents based on intent.
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.routing_table: Dict[str, Agent] = {}

    def register_agent(self, intent: str, agent: Agent):
        """Register a specialist agent for a specific intent."""
        self.routing_table[intent] = agent

    async def route_task(self, intent: str) -> Optional[Agent]:
        """Find the agent responsible for the given intent."""
        return self.routing_table.get(intent)

    async def process_message(self, message: AgentMessage) -> None:
        """
        Process incoming messages.
        """
        if message.type == "request":
            intent = message.metadata.get("intent")
            if not intent:
                return  # Log warning: missing intent

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
                pass  # Log warning: no route found

        elif message.type == "response":
            # Forward response back to the original requester
            reply_to = message.metadata.get("reply_to")
            if reply_to:
                # Resolve recipient using Registry (via _resolve_agent helper or Registry directly)
                from arkhon_rheo.core.registry import AgentRegistry

                target_agent = AgentRegistry.get(reply_to)

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
                    pass
            else:
                pass
