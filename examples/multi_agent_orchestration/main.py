import asyncio
from dataclasses import asdict

from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.message import AgentMessage
from arkhon_rheo.core.runtime.scheduler import RuntimeScheduler
from arkhon_rheo.core.state import AgentState


class Researcher(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.last_result = ""

    async def process_message(self, message: AgentMessage) -> None:
        self.last_result = f"Research results for: {message.content}"


class Writer(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.last_result = ""

    async def process_message(self, message: AgentMessage) -> None:
        self.last_result = f"Draft based on: {message.content}"


async def research_node(state: AgentState):
    agent = Researcher(name="researcher")
    # Get last message
    last_msg_dict = state["messages"][-1]
    last_msg = AgentMessage(**last_msg_dict)

    await agent.process_message(last_msg)
    res = agent.last_result

    new_msg = AgentMessage(
        sender="researcher", receiver="writer", content=res, type="info"
    )
    return {"messages": [asdict(new_msg)]}


async def write_node(state: AgentState):
    agent = Writer(name="writer")
    last_msg_dict = state["messages"][-1]
    last_msg = AgentMessage(**last_msg_dict)

    await agent.process_message(last_msg)
    res = agent.last_result

    new_msg = AgentMessage(sender="writer", receiver="user", content=res, type="info")
    return {"messages": [asdict(new_msg)], "is_completed": True}


def create_orchestration_graph():
    graph = Graph()
    graph.add_node("research", research_node)
    graph.add_node("write", write_node)

    graph.add_edge("research", "write")
    return graph


async def main():
    graph = create_orchestration_graph()
    scheduler = RuntimeScheduler(graph, checkpoint_manager=None)

    initial_message = AgentMessage(
        sender="user",
        receiver="researcher",
        content="The history of AI",
        type="request",
    )

    state: AgentState = {
        "messages": [asdict(initial_message)],
        "next_step": "research",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "example_thread",
    }

    print("🚀 Starting Refactored Multi-Agent Flow...")
    await scheduler.run(state, entry_point="research")

    print("\n--- Message History ---")
    for msg_dict in state["messages"]:
        m = AgentMessage(**msg_dict)
        print(f"[{m.sender} -> {m.receiver}]: {m.content[:50]}...")


if __name__ == "__main__":
    asyncio.run(main())
