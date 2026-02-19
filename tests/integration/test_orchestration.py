import asyncio

import pytest

from arkhon_rheo.agents.coordinator import CoordinatorAgent
from arkhon_rheo.agents.specialist import SpecialistAgent

# Mock User Agent to send request and receive response
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage
from arkhon_rheo.core.registry import AgentRegistry
from arkhon_rheo.runtime.scheduler import AgentScheduler


class UserAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.received_messages = []
        self.completion_event = asyncio.Event()

    async def process_message(self, message: AgentMessage):
        self.received_messages.append(message)
        if message.type == "response":
            self.completion_event.set()


@pytest.mark.asyncio
async def test_orchestration_flow():
    # Clear registry for test isolation
    AgentRegistry.clear()

    # Setup Agents (they auto-register)
    user = UserAgent("user")
    coordinator = CoordinatorAgent("coordinator")
    specialist = SpecialistAgent("coder", domain="coding")

    # Configure Routing
    coordinator.register_agent("write_code", specialist)

    # Setup Scheduler
    scheduler = AgentScheduler()
    scheduler.register_agent(user)
    scheduler.register_agent(coordinator)
    scheduler.register_agent(specialist)

    # Task
    task_msg = AgentMessage(
        sender="user",
        receiver="coordinator",
        content="implement hello world",
        type="request",
        metadata={"intent": "write_code"},
    )

    # Start Protocol
    await user.send_message(coordinator, task_msg)

    # Run Scheduler until User gets a response
    # We create a task that waits for user.completion_event
    await scheduler.run_until_complete(user.completion_event.wait())

    # Verify
    assert len(user.received_messages) == 1
    response = user.received_messages[0]
    # The response comes from coordinator (proxy) or specialist?
    # Coordinator forwards response, so sender should be coordinator or specialist depending on implementation?
    # In my fix: forwarded_msg = AgentMessage(sender=self.name...) -> sender is coordinator
    assert response.sender == "coordinator"
    assert "coding specialist" in response.content
    assert (
        response.metadata.get("reply_to") == "user"
    )  # Consumed by coordinator or not present on final response to user?
    # Actually Coordinator sends: sender=self.name, receiver=target.name.
    # When Specialist replies: receiver=message.sender (Coordinator).
    # Coordinator forwards: sender=self.name, receiver=target_agent (User).
    # So user sees sender="coordinator".
