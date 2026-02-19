import pytest

from arkhon_rheo.agents.specialist import SpecialistAgent
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


@pytest.mark.asyncio
async def test_specialist_processing():
    # Register a coordinator for the specialist to find in the registry
    SpecialistAgent("coordinator", domain="general")
    agent = SpecialistAgent("coder", domain="coding")
    msg = AgentMessage(
        sender="coordinator",
        receiver="coder",
        content="write python code",
        type="request",
    )

    # Track replies
    replies = []

    async def mock_send(_recipient: Agent, message: AgentMessage) -> None:

        replies.append(message)

    agent.send_message = mock_send  # type: ignore

    await agent.process_message(msg)

    assert len(replies) == 1
    reply = replies[0]
    assert reply.type == "response"
    assert "Processed by coding specialist" in str(reply.content)
