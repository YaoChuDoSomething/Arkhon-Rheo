import pytest

from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage
from arkhon_rheo.core.registry import AgentRegistry


class EchoAgent(Agent):
    async def process_message(self, message: AgentMessage):
        if message.type == "ping":
            reply = AgentMessage(
                sender=self.name,
                receiver=message.sender,
                content="pong",
                type="pong",
                correlation_id=message.id,
            )
            # Use registry from singleton
            recipient = AgentRegistry.get(message.sender)
            if recipient:
                await self.send_message(recipient, reply)


class StarterAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.received_replies = []

    async def process_message(self, message: AgentMessage):
        self.received_replies.append(message)


@pytest.mark.asyncio
async def test_agent_conversation():
    AgentRegistry.clear()

    agent_a = StarterAgent("A")
    agent_b = EchoAgent("B")

    # Auto-registered via __init__

    # Start message
    msg = AgentMessage(sender="A", receiver="B", content="ping", type="ping")

    await agent_a.send_message(agent_b, msg)

    # Process B's inbox manually for test control
    msg_for_b = await agent_b.receive_message()
    await agent_b.process_message(msg_for_b)

    # Process A's inbox
    msg_for_a = await agent_a.receive_message()
    await agent_a.process_message(msg_for_a)

    assert len(agent_a.received_replies) == 1
    reply = agent_a.received_replies[0]
    assert reply.content == "pong"
    assert reply.sender == "B"
    assert reply.correlation_id == msg.id
