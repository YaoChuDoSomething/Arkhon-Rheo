import asyncio

from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class SimpleMathAgent(Agent):
    """An agent that performs basic arithmetic reasoning."""

    def __init__(self, name: str):
        super().__init__(name)
        self.last_response = ""

    async def process_message(self, message: AgentMessage) -> None:
        content = message.content.lower()
        if "add" in content:
            self.last_response = "Thinking... I should add these numbers."
        else:
            self.last_response = f"Echoing back: {message.content}"


async def main():
    # Initialize the agent
    agent = SimpleMathAgent(name="math-bot")

    # Simulate a request
    request = AgentMessage(
        sender="User", receiver="math-bot", content="Add 2 and 3", type="request"
    )

    print(f"User: {request.content}")
    await agent.process_message(request)
    response = agent.last_response
    print(f"MathBot: {response}")


if __name__ == "__main__":
    asyncio.run(main())
