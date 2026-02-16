import asyncio
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


# Define state for LangGraph
class GraphState(TypedDict):
    messages: list[AgentMessage]
    next_step: str


class Researcher(Agent):
    async def process_message(self, message: AgentMessage) -> str:
        return f"Research results for: {message.content}"


class Writer(Agent):
    async def process_message(self, message: AgentMessage) -> str:
        return f"Draft based on: {message.content}"


async def research_node(state: GraphState):
    agent = Researcher(name="researcher")
    msg = state["messages"][-1]
    res = await agent.process_message(msg)
    state["messages"].append(
        AgentMessage(sender="researcher", receiver="writer", content=res, type="info")
    )
    state["next_step"] = "write"
    return state


async def write_node(state: GraphState):
    agent = Writer(name="writer")
    msg = state["messages"][-1]
    res = await agent.process_message(msg)
    state["messages"].append(
        AgentMessage(sender="writer", receiver="user", content=res, type="info")
    )
    state["next_step"] = "end"
    return state


def create_orchestration_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)

    workflow.add_edge(START, "research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", END)

    return workflow.compile()


async def main():
    graph = create_orchestration_graph()
    initial_message = AgentMessage(
        sender="user",
        receiver="researcher",
        content="The history of AI",
        type="request",
    )

    print("🚀 Starting Multi-Agent Flow...")
    final_state = await graph.ainvoke(
        {"messages": [initial_message], "next_step": "start"}
    )

    for msg in final_state["messages"]:
        print(f"[{msg.sender} -> {msg.receiver}]: {msg.content[:50]}...")


if __name__ == "__main__":
    asyncio.run(main())
