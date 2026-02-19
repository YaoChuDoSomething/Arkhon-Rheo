from unittest.mock import AsyncMock, patch

import pytest

from arkhon_rheo.agents.coordinator import CoordinatorAgent
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class MockAgent(Agent):
    async def process_message(self, message: AgentMessage):
        pass


@pytest.mark.asyncio
async def test_coordinator_routing():
    coordinator = CoordinatorAgent("coordinator")
    specialist = MockAgent("spec-1")

    coordinator.register_agent("intent_a", specialist)

    msg = AgentMessage(
        sender="user",
        receiver="coordinator",
        content="do task A",
        type="request",
        metadata={"intent": "intent_a"},
    )

    # Mock send_message to verify routing
    with patch.object(
        CoordinatorAgent, "send_message", new_callable=AsyncMock
    ) as mock_send:
        await coordinator.process_message(msg)

        # Should route to spec-1
        mock_send.assert_called_once()
        args, _ = mock_send.call_args
        recipient, forwarded_msg = args

        assert recipient.name == "spec-1"
        assert forwarded_msg.content == "do task A"
        assert forwarded_msg.sender == "coordinator"


@pytest.mark.asyncio
async def test_coordinator_no_route():
    coordinator = CoordinatorAgent("coordinator")
    msg = AgentMessage(
        sender="user",
        receiver="coordinator",
        content="unknown task",
        type="request",
        metadata={"intent": "unknown"},
    )

    with patch.object(
        CoordinatorAgent, "send_message", new_callable=AsyncMock
    ) as mock_send:
        await coordinator.process_message(msg)
        mock_send.assert_not_called()
