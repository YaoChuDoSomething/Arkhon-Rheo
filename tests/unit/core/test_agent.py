import pytest
import asyncio
from unittest.mock import AsyncMock
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class MockAgent(Agent):
    async def process_message(self, message: AgentMessage):
        pass


@pytest.mark.asyncio
async def test_agent_initialization():
    agent = TestAgent(name="test-agent")
    assert agent.name == "test-agent"
    assert isinstance(agent.inbox, asyncio.Queue)


@pytest.mark.asyncio
async def test_agent_send_message():
    sender = TestAgent(name="sender")
    receiver = TestAgent(name="receiver")
    msg = AgentMessage(
        sender=sender.name, receiver=receiver.name, content="hello", type="request"
    )

    await sender.send_message(receiver, msg)

    # Check if receiver got the message
    received_msg = await receiver.inbox.get()
    assert received_msg == msg


@pytest.mark.asyncio
async def test_agent_receive_message():
    agent = TestAgent(name="agent")
    msg = AgentMessage(
        sender="sender", receiver="agent", content="hello", type="request"
    )

    await agent.inbox.put(msg)

    received_msg = await agent.receive_message()
    assert received_msg == msg
