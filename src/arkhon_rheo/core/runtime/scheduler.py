import asyncio
from typing import Any, Dict, Optional
from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.state import AgentState


class RuntimeScheduler:
    """
    Asynchronous executor for the agentic graph with checkpointing support.
    """

    def __init__(self, graph: Graph, checkpoint_manager: Any):
        self.graph = graph
        self.checkpoint_manager = checkpoint_manager

    async def step(self, current_node: str, state: AgentState) -> str:
        """
        Execute a single node and determine the next transition.
        Updates the state and persists it via high-security checkpointing.
        """
        if current_node not in self.graph.nodes:
            return "END"

        # Node execution: nodes return a delta dict or full state
        action = self.graph.nodes[current_node]
        try:
            result = action(state)
            if asyncio.iscoroutine(result):
                result = await result

            # Update state with delta
            if isinstance(result, dict):
                # Apply delta. Note: operator.add in TypedDict usually requires
                # specific handling if we're not using a framework like LangGraph
                # for simple dict updates we simulate accumulation here if needed.
                for k, v in result.items():
                    if k == "messages" and k in state:
                        state[k] = state[k] + v
                    else:
                        state[k] = v
        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(str(e))
            return "END"

        # Checkpoint persistence
        if self.checkpoint_manager:
            self.checkpoint_manager.save_checkpoint(state)

        # Routing logic: Conditional Edges take precedence
        if current_node in self.graph.conditional_edges:
            cond_cfg = self.graph.conditional_edges[current_node]
            decision = cond_cfg["fn"](state)
            return cond_cfg["map"].get(decision, "END")

        # Static routing
        for start, end in self.graph.edges:
            if start == current_node:
                return end

        return "END"

    async def run(self, initial_state: AgentState, entry_point: str):
        """
        Main control loop (The Engine).
        """
        curr = entry_point
        while curr != "END" and not initial_state.get("is_completed"):
            curr = await self.step(curr, initial_state)
        return initial_state
