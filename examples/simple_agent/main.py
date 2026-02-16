import asyncio
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class SimpleMathAgent(Agent):
    """An agent that performs basic arithmetic reasoning."""

    async def process_message(self, message: AgentMessage) -> str:
        content = message.content.lower()
        if "add" in content:
            return "Thinking... I should add these numbers."
        return f"Echoing back: {message.content}"


async def main():
    # Initialize the agent
    agent = SimpleMathAgent(name="math-bot")

    # Simulate a request
    request = AgentMessage(
        sender="User", receiver="math-bot", content="Add 2 and 3", type="request"
    )

    print(f"User: {request.content}")
    response = await agent.process_message(request)
    print(f"MathBot: {response}")


if __name__ == "__main__":
    asyncio.run(main())
