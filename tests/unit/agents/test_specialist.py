import pytest
from arkhon_rheo.agents.specialist import SpecialistAgent
from arkhon_rheo.core.message import AgentMessage


@pytest.mark.asyncio
async def test_specialist_processing():
    agent = SpecialistAgent("coder", domain="coding")
    msg = AgentMessage(
        sender="coordinator",
        receiver="coder",
        content="write python code",
        type="request",
    )

    # Track replies
    replies = []

    async def mock_send(recipient: "Agent", message: AgentMessage) -> None:
        replies.append(message)

    agent.send_message = mock_send  # type: ignore

    await agent.process_message(msg)

    assert len(replies) == 1
    reply = replies[0]
    assert reply.type == "response"
    assert "Processed by coding specialist" in str(reply.content)
